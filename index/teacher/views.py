from index.models import Teacher, Discipline, TeacherDetails, TeacherLessonConstraint
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from django_filters.rest_framework import FilterSet, CharFilter
from index.lesson.views import SpecDisciplineSerializer
from django.db.models import Q
from rest_framework.decorators import action

class TeacherLessonConstraintSerializer(serializers.Serializer):
    teacher_id = serializers.IntegerField(required=False)
    id = serializers.IntegerField(required=False)
    lesson = serializers.IntegerField()
    day_of_week = serializers.IntegerField()
    remove = serializers.BooleanField(default=False)


class TeacherSerializer(serializers.ModelSerializer):
    disciplines = SpecDisciplineSerializer(many=True)
    constraints = TeacherLessonConstraintSerializer(many=True)

    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'disciplines', 'constraints', 'total_hours']

    def _set_lesson_constraints(self, constraints, pk):
        ids_to_delete = []
        constraints_to_create = []
        for constraint in constraints:
            if constraint.get('id'):
                if constraint.get('remove'):
                    ids_to_delete.append(constraint['id'])
                continue
            constraints_to_create.append(
                TeacherLessonConstraint(
                    lesson=constraint['lesson'],
                    day_of_week=constraint['day_of_week'],
                    teacher_id=pk,
                )
            )
        TeacherLessonConstraint.objects.filter(id__in=ids_to_delete).delete()
        TeacherLessonConstraint.objects.bulk_create(constraints_to_create)

        return True

    def create(self, validated_data):
        constraints = validated_data.pop('constraints', None)
        teacher = super().create(validated_data)
        if constraints:
            self._set_lesson_constraints(constraints, teacher.id)
        return teacher

    def update(self, instance, validated_data):
        constraints = validated_data.pop('constraints', None)
        teacher = super().update(instance, validated_data)
        if constraints:
            self._set_lesson_constraints(constraints, teacher.id)
        return teacher


class TeacherFilter(FilterSet):
    name = CharFilter(field_name='first_name', method='filter_name')
    
    def filter_name(self, queryset, name, value):
        values = value.split(',')
        q = Q()
        for val in values:
            q |= Q(first_name__icontains=val)
            q |= Q(last_name__icontains=val)
            q |= Q(middle_name__icontains=val)
        return queryset.filter(q)

    class Meta:
        model = Teacher
        fields = {
            'name': ['exact',],
            'disciplines': ['exact'],
        }

        
class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
    filterset_class = TeacherFilter

    def create(self, request):
        data = TeacherSerializer(data=request.data)

        data.is_valid(raise_exception=True)

        disciplines_ids = data.validated_data.pop('disciplines', [])

        data.save()

        teacher = data.instance

        details = [
            TeacherDetails(teacher=teacher,
            discipline_id=discipline['id'])
            for discipline in disciplines_ids
        ]

        TeacherDetails.objects.bulk_create(details)

        return Response(TeacherSerializer(instance=teacher).data, status=201)

    
    def update(self, request, pk=None):
        teacher = Teacher.objects.get(pk=pk)

        data = TeacherSerializer(data=request.data, instance=teacher)

        data.is_valid(raise_exception=True)

        disciplines_ids = list(map(lambda x: x['id'], data.validated_data.pop('disciplines', [])))

        data.save()

        teacher.details.exclude(discipline_id__in=disciplines_ids).delete()
        for d in teacher.details.all():
            disciplines_ids.remove(d.discipline_id)

        details = [
            TeacherDetails(teacher=teacher,
            discipline_id=discipline_id)
            for discipline_id in disciplines_ids
        ]

        TeacherDetails.objects.bulk_create(details)

        return Response(TeacherSerializer(instance=teacher).data)        
