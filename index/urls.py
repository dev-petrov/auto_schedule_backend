from django.conf.urls import url, include
from rest_framework import routers
from index.discipline.views import DisciplineViewSet
from index.education_plan.views import EducationPlanViewSet
from index.group.views import GroupViewSet
from index.lecture_hall.views import LectureHallViewSet
from index.lesson.views import LessonViewSet
from index.teacher.views import TeacherViewSet
from index.training_direction.views import TrainingDirectionViewSet


router = routers.DefaultRouter()
router.register(r'discipline', DisciplineViewSet, basename='Discipline')
router.register(r'education_plan', EducationPlanViewSet, basename='EducationPlan')
router.register(r'group', GroupViewSet, basename='Group')
router.register(r'lecture_hall', LectureHallViewSet, basename='LectureHall')
router.register(r'lesson', LessonViewSet, basename='Lesson')
router.register(r'teacher', TeacherViewSet, basename='Teacher')
router.register(r'training_direction', TrainingDirectionViewSet, basename='TrainingDirection')


urlpatterns = [
    url(r'^', include(router.urls)),
]

