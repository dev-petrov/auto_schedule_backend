from index.models import Lesson
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from index.group.views import GroupSerializer
from index.discipline.views import DisciplineSerializer
from index.teacher.views import TeacherSerializer
from index.lecture_hall.views import LectureHallSerializer
from django.db.models import Q
from django_filters.rest_framework import FilterSet, CharFilter


class LessonSerializer(serializers.ModelSerializer):
    discipline = DisciplineSerializer()
    group = GroupSerializer()
    teacher = TeacherSerializer()
    lecture_hall = LectureHallSerializer()

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