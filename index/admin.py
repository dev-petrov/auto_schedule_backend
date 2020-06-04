from django.contrib import admin
from index.models import (
    Group, 
    Flow, 
    Lesson,
    Teacher,
    Discipline,
    EducationPlan,
    TrainingDirection,
    ConstraintCollection,
    LectureHall,
    TeacherDetails,
) 
# Register your models here.

admin.site.register(Group)
admin.site.register(Flow)
admin.site.register(Lesson)
admin.site.register(Teacher)
admin.site.register(Discipline)
admin.site.register(EducationPlan)
admin.site.register(TrainingDirection)
admin.site.register(ConstraintCollection)
admin.site.register(LectureHall)
admin.site.register(TeacherDetails)

