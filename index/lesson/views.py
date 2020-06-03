from index.models import Lesson, Teacher, Group, EducationPlan, LectureHall, Discipline
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from django.db.models import Q, F
from django_filters.rest_framework import FilterSet, CharFilter


class SpecTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'middle_name']


class SpecGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'code']


class SpecDisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ['id', 'title']


class SpecEducationPlanSerializer(serializers.ModelSerializer):
    discipline = SpecDisciplineSerializer()
    class Meta:
        model = EducationPlan
        fields = ['id', 'discipline', 'hours', 'type']


class SpecLectureHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureHall
        fields = ['id', 'code', 'building', 'prof_type']


class LessonSerializer(serializers.ModelSerializer):
    discipline = SpecEducationPlanSerializer(read_only=True)
    group = SpecGroupSerializer(read_only=True)
    teacher = SpecTeacherSerializer(read_only=True)
    lecture_hall = SpecLectureHallSerializer(read_only=True)
    discipline_id = serializers.IntegerField(write_only=True)
    group_id = serializers.IntegerField(write_only=True)
    teacher_id = serializers.IntegerField(write_only=True)
    lecture_hall_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonFilter(FilterSet):
    discipline = CharFilter(field_name='discipline', lookup_expr='title__icontains')
    group = CharFilter(field_name='group', lookup_expr='code__icontains')
    teacher = CharFilter(field_name='teacher', method='filter_teacher')
    lecture_hall = CharFilter(field_name='lecture_hall', lookup_expr='code__icontains')


    def filter_teacher(self, queryset, name, value):
        
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(middle_name__icontains=value)
        )
    class Meta:
        model = Lesson
        fields = {
            'discipline':['exact'],
            'group': ['exact'],
            'teacher': ['exact'],
            'lecture_hall': ['exact'],
        }

        
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()   
    serializer_class = LessonSerializer
    filterset_class = LessonFilter

    def list(self, request):
        query = self.filter_queryset(self.queryset).select_related('discipline', 'lecture_hall', 'teacher', 'group', 'discipline__discipline')
        dtype = request.query_params.get('dtype', 'a')
        if dtype.lower() == 't':
            lessons = list(query.order_by('teacher_id', 'day_of_week', 'lesson'))
            data = {}
            for lesson in lessons:
                key = lesson.teacher_id
                if not key in data:
                    data[key] = []
                data[key].append(
                    LessonSerializer(lesson).data
                )
        elif dtype.lower() == 'g':
            lessons = list(query.order_by('group_id', 'day_of_week', 'lesson'))
            data = {}
            for lesson in lessons:
                key = lesson.group_id
                if not key in data:
                    data[key] = []
                data[key].append(
                    LessonSerializer(lesson).data
                )
        else:
            data = LessonSerializer(query.order_by('group_id', 'day_of_week', 'lesson'), many=True).data
        return Response(data)
    