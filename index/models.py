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

    title = models.CharField(max_length=100)
    prof_type = models.CharField(max_length=1, choices=PROF_TYPES, default=PROF_TYPE_SIMPLE)
    constraints = models.ForeignKey(ConstraintCollection, on_delete=models.PROTECT)


class Teacher(models.Model):

    BUILD_VDNH = 'V'
    BUILD_AUTAZ = 'A'
    BUILD_ELECTRO = 'E'
    BUILD_PRYANIKI = 'P'
    BUILD_SADOVAYA = 'S'

    BUILDINGS = [
        (BUILD_VDNH, 'ул. Павла Корчагина'),
        (BUILD_AUTAZ, 'ул. Автозаводская'),
        (BUILD_ELECTRO, 'ул. Большая Семеновская'),
        (BUILD_PRYANIKI, 'ул. Прянишникова'),
        (BUILD_SADOVAYA, 'ул. Садовая-Спасская'),
    ]
    def_constraints = {
        'buildings_priority': [
            BUILD_ELECTRO, 
            BUILD_AUTAZ, 
            BUILD_VDNH, 
            BUILD_SADOVAYA, 
            BUILD_PRYANIKI,
        ],
        'day_constraints': default_day_constraints,
    }

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    disciplines = models.ManyToManyField(Discipline, through='TeacherDetails')
    constraints = models.TextField(default=json.dumps(def_constraints))
    total_hours = models.IntegerField()


class TrainingDirection(models.Model):

    TYPE_BACHELOR = 'B'
    TYPE_SPECIALTY = 'S'
    TYPE_MAGISTRACY = 'M'

    TYPES = [
        (TYPE_BACHELOR, 'Бакалавриат'),
        (TYPE_SPECIALTY, 'Специалитет'),
        (TYPE_MAGISTRACY, 'Магистратура'),
    ]

    def_constraints = {
        'buildings':[
            Teacher.BUILD_ELECTRO, 
            Teacher.BUILD_AUTAZ, 
            Teacher.BUILD_PRYANIKI, 
            Teacher.BUILD_VDNH, 
            Teacher.BUILD_SADOVAYA,
        ],
        'day_constraints': default_day_constraints,
    }

    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

    type = models.CharField(max_length=1, choices=TYPES, default=TYPE_BACHELOR)

    constraints = models.TextField(verbose_name='Ограничения направления', default=json.dumps(def_constraints))


class Flow(models.Model):
    name = models.CharField(max_length=200)


class Group(models.Model):
    code = models.CharField(max_length=7)
    count_of_students = models.IntegerField()
    training_direction = models.ForeignKey(TrainingDirection, on_delete=models.PROTECT)

    flow = models.ForeignKey(Flow, on_delete=models.PROTECT)
    constraints = models.TextField(default=json.dumps(default_day_constraints))


class EducationPlan(models.Model):
    TYPE_LECTION = 'L'
    TYPE_PRACTICE = 'P'
    TYPE_LAB = 'LB'

    TYPES = [
        (TYPE_LECTION, 'Лекция'),
        (TYPE_PRACTICE, 'Практика'),
        (TYPE_LAB, 'Лаб. работа'),
    ]

    discipline = models.ForeignKey(Discipline, on_delete=models.PROTECT)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    type = models.CharField(max_length=2, choices=TYPES, default=TYPE_LECTION)

    hours = models.IntegerField()
    constraints = models.TextField(null=True)


class LectureHall(models.Model):
    spaciousness = models.IntegerField()
    code = models.CharField(max_length=10)
    building = models.CharField(max_length=1, choices=Teacher.BUILDINGS, default=Teacher.BUILD_ELECTRO)
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
    discipline = models.ForeignKey(EducationPlan, on_delete=models.PROTECT)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    lecture_hall = models.ForeignKey(LectureHall, on_delete=models.PROTECT)
    lesson = models.IntegerField(choices=LESSONS, default=1)
    day_of_week = models.IntegerField(choices=DAY_OF_WEEK, default=1)


class TeacherDetails(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.PROTECT)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='details')
