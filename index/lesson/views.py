from index.models import Lesson
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from index.group.views import GroupSerializer
from index.discipline.views import DisciplineSerializer
from index.teacher.views import TeacherSerializer
from index.lecture_hall.views import LectureHallSerializer


class LessonSerializer(serializers.ModelSerializer):
    discipline = DisciplineSerializer()
    group = GroupSerializer()
    teacher = TeacherSerializer()
    lecture_hall = LectureHallSerializer()

    class Meta:
        model = Lesson
        fields = '__all__'

        
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()   
