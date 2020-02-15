from django.db import models


class Discipline(models.Model):

    TYPE_LECTION = 'L'
    TYPE_PRACTICE = 'P'
    TYPE_LAB = 'LB'

    TYPES = [
        (TYPE_LECTION, 'Лекция'),
        (TYPE_PRACTICE, 'Практика'),
        (TYPE_LAB, 'Лаб. работа'),
    ]

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
    type = models.CharField(max_length=2, choices=TYPES, default=TYPE_LECTION)
    prof_type = models.CharField(max_length=1, choices=PROF_TYPES, default=PROF_TYPE_SIMPLE)
    need_projector = models.BooleanField()
    need_big_blackboard = models.BooleanField()


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

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    disciplines = models.ManyToManyField(Discipline)
    constraints = models.TextField()
    building = models.CharField(max_length=1, choices=BUILDINGS, default=BUILD_ELECTRO)
