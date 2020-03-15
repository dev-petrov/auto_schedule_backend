from index.models import Teacher, Discipline
from discipline.views import DisciplineSerializer
from rest_framework import serializers, viewsets
from rest_framework.response import Response

class TeacherSerializer(serializers.ModelSerializer):
    disciplines = DisciplineSerializer(many=True, read_only=True)
    constraints = serializers.JSONField()
    disciplines_ids = serializers.ListField(write_only=True)

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'middle_name', 'disciplines', 'constraints', 'total_hours', 'disciplines_ids']

        
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.prefetch_related('disciplines').all()

    def create(self, request):
        data = TeacherSerializer(data=request.data)

        data.is_valid(raise_exception=True)

        disciplines_ids = data.validated_data.pop('disciplines_ids', [])

        data.save()

        teacher = data.instance

        for discipline in Discipline.objects.filter(id__in=disciplines_ids):
            teacher.disciplines.add(discipline)

        return Response(TeacherSerializer(instance=teacher).data)

    
    def update(self, request, pk=None):
        teacher = Teacher.objects.get(pk=pk)

        data = TeacherSerializer(data=request.data, instance=teacher)

        data.is_valid(raise_exception=True)

        disciplines_ids = data.validated_data.pop('disciplines_ids', [])

        data.save()

        teacher_disciplines = list(teacher.objects.disciplines.all())

        for discipline in teacher_disciplines:
            if discipline.id not in disciplines_ids:
                 teacher.objects.disciplines.remove(discipline)

        teacher_disciplines = list(teacher.objects.disciplines.all())

        for discipline in Discipline.objects.filter(id__in=disciplines_ids):
            if discipline not in teacher_disciplines:
                teacher.disciplines.add(discipline)

        return Response(TeacherSerializer(instance=teacher).data)
    
