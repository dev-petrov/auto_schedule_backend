from django.db import models
from index.defaults import default_day_constraints
import json


class ConstraintCollection(models.Model):
    class Meta:
        unique_together = ['projector', 'big_blackboard']
    projector = models.BooleanField(default=False)
    big_blackboard = models.BooleanField(default=False)


class Discipline(models.Model):

    PROF_TYPE_SIMPLE = 'S'
    PROF_TYPE_COMP = 'C'
    PROF_TYPE_DESIGN = 'D'
    PROF_TYPE_LAB = 'L'
    PROF_TYPE_MECHANIC = 'M'

    PROF_TYPES = [
        (PROF_TYPE_SIMPLE, 'Обычная'),
        (PROF_TYPE_COMP, 'Компьютерная'),
        (PROF_TYPE_DESIGN, 'Дизайн'),
        (PROF_TYPE_LAB, 'Лаборатория'),
        (PROF_TYPE_MECHANIC, 'Мастерская'),
    ]

    TYPE_LECTION = 'L'
    TYPE_PRACTICE = 'P'
    TYPE_LAB = 'LB'

    TYPES = [
        (TYPE_LECTION, 'Лекция'),
        (TYPE_PRACTICE, 'Практика'),
        (TYPE_LAB, 'Лаб. работа'),
    ]

    title = models.CharField(max_length=100)
    prof_type = models.CharField(max_length=1, choices=PROF_TYPES, default=PROF_TYPE_SIMPLE)
    constraints = models.ForeignKey(ConstraintCollection, on_delete=models.PROTECT)
    type = models.CharField(max_length=2, choices=TYPES, default=TYPE_LECTION)
    short_name = models.CharField(max_length=8)


class Building(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=32)
    primary_color = models.CharField(max_length=7)
    secondary_color = models.CharField(max_length=7)


class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    disciplines = models.ManyToManyField(Discipline, through='TeacherDetails', related_name='teachers')
    total_hours = models.IntegerField()

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'


class TeacherLessonConstraint(models.Model):
    class Meta:
        unique_together = ['lesson', 'day_of_week', 'teacher']
    lesson = models.IntegerField()
    day_of_week = models.IntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='constraints')


class TrainingDirection(models.Model):

    TYPE_BACHELOR = 'B'
    TYPE_SPECIALTY = 'S'
    TYPE_MAGISTRACY = 'M'

    TYPES = [
        (TYPE_BACHELOR, 'Бакалавриат'),
        (TYPE_SPECIALTY, 'Специалитет'),
        (TYPE_MAGISTRACY, 'Магистратура'),
    ]


    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

    type = models.CharField(max_length=1, choices=TYPES, default=TYPE_BACHELOR)

class LessonTrainingDirectionConstraint(models.Model):
    class Meta:
        unique_together = ['lesson', 'day_of_week', 'training_direction']
    lesson = models.IntegerField()
    day_of_week = models.IntegerField()
    training_direction = models.ForeignKey(TrainingDirection, on_delete=models.CASCADE, related_name='constraints')


class BuildingTrainingDirectionConstraint(models.Model):
    class Meta:
        unique_together = ['building', 'training_direction']
    building = models.ForeignKey(Building, on_delete=models.PROTECT)
    training_direction = models.ForeignKey(TrainingDirection, on_delete=models.CASCADE, related_name='building_constraints')
    ordering = models.IntegerField()

class Flow(models.Model):
    name = models.CharField(max_length=200)


class Group(models.Model):
    code = models.CharField(max_length=7)
    count_of_students = models.IntegerField()
    training_direction = models.ForeignKey(TrainingDirection, on_delete=models.PROTECT)
    disciplines = models.ManyToManyField(Discipline, through='EducationPlan', related_name='groups')
    flow = models.ForeignKey(Flow, on_delete=models.PROTECT, null=True, blank=True)


class EducationPlan(models.Model):

    discipline = models.ForeignKey(Discipline, on_delete=models.PROTECT)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    lessons_in_week = models.IntegerField()

    def __str__(self):
        return '{} {} {}'.format(
            self.discipline.title,
            self.group.code,
            self.hours,
        )

class LectureHall(models.Model):
    spaciousness = models.IntegerField()
    code = models.CharField(max_length=10)
    building = models.ForeignKey(Building, on_delete=models.PROTECT)
    prof_type = models.CharField(max_length=1, choices=Discipline.PROF_TYPES, default=Discipline.PROF_TYPE_SIMPLE)
    constraints = models.ForeignKey(ConstraintCollection, on_delete=models.PROTECT)


class Lesson(models.Model):
    LESSONS = [
        (1, 'Первая пара'),
        (2, 'Вторая пара'),
        (3, 'Третья пара'),
        (4, 'Четвёртая пара'),
        (5, 'Пятая пара'),
        (6, 'Шестая пара'),
        (7, 'Седьмая пара'),
    ]

    DAY_OF_WEEK = [
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
    ]
    discipline = models.ForeignKey(Discipline, on_delete=models.PROTECT)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    lecture_hall = models.ForeignKey(LectureHall, on_delete=models.PROTECT)
    lesson = models.IntegerField(choices=LESSONS, default=1)
    day_of_week = models.IntegerField(choices=DAY_OF_WEEK, default=1)


class TeacherDetails(models.Model):

    class Meta:
        unique_together = ('discipline', 'teacher')

    discipline = models.ForeignKey(Discipline, on_delete=models.PROTECT)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='details')
