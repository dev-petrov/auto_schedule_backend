from django.conf.urls import url, include
from rest_framework import routers
from index.discipline.views import DisciplineViewSet
from index.education_plan.views import EducationPlanViewSet
from index.group.views import GroupViewSet
from index.lecture_hall.views import LectureHallViewSet
from index.lesson.views import LessonViewSet
from index.teacher.views import TeacherViewSet
from index.training_direction.views import TrainingDirectionViewSet
from index.building.views import BuildingViewSet
from index.flow.views import FlowViewSet
from rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView, UserDetailsView,
)

rest_auth_urls = [
    url(r'^login/$', LoginView.as_view(), name='rest_login'),
    url(r'^logout/$', LogoutView.as_view(), name='rest_logout'),
    url(r'^password/change/$', PasswordChangeView.as_view(), name='rest_password_change'),
    url(r'^user/$', UserDetailsView.as_view(), name='user'),
]

router = routers.DefaultRouter()
router.register(r'discipline', DisciplineViewSet, basename='Discipline')
router.register(r'education_plan', EducationPlanViewSet, basename='EducationPlan')
router.register(r'group', GroupViewSet, basename='Group')
router.register(r'lecture_hall', LectureHallViewSet, basename='LectureHall')
router.register(r'lesson', LessonViewSet, basename='Lesson')
router.register(r'teacher', TeacherViewSet, basename='Teacher')
router.register(r'training_direction', TrainingDirectionViewSet, basename='TrainingDirection')
router.register(r'flow', FlowViewSet, basename='Flow')
router.register(r'building', BuildingViewSet, basename='Building')



urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include((rest_auth_urls,'auth'),namespace='auth')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

