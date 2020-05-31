from index.models import *
import json
import random
import codecs
from index.models import ConstraintCollection
'''
Модуль для заполнения базы данных тестовыми данными.

Здесь создаются:
Дисциплины:
    Математика (нужна большая доска, обычная аудитория)
    Физика (нужна большая доска, нужен проектор, обычная аудитория)
    ....
    Необходимо создать 30 дисциплин (должны использоваться все возможные типы проф дисциплин)

Преподаватели:
    1. для каждой дисциплины должно быть минимум 2 преподавателя
    2. один преподаватель может вести несколько дисциплин

Направления подготовки:
    Задать 10 направлений подготовки
    Здесь же при помощи ограничений по дням-парам можно задать
    ограничения типа очно, очно-заочно

Группы:
    Сделать 50 групп, для каждого направления подготовки на 5 лет
    Сделать 20 групп для некоторых курсов, чтобы объеденить в потоки (логичнее для 1-2 курса)

Потоки:
    Объеденить в потоки группы с одинаковым направлением и одинаковым курсом

План обучения:
    Составить для каждой группы план обучения в соответсвии с направлением
    Ограничения пока не продуманы, оставить поле пустым

Аудитории:
    Необходимо создать аудитории с небольшим избытком (учитывая потребность
    в проф аудитории, проекторе, большой доске)


'''
path = 'scripts/data.json'

def Main():
    Set_Disciplines()
    Set_EducationPlans()
    Set_Flows()
    Set_Groups()
    Set_LectureHalls()
    Set_Teachers()
    Set_TrainingDirections()

def Set_Disciplines():
    with codecs.open(path, 'r', 'utf_8_sig') as f:
        data = json.loads(f.read())
        for d in data['Discipline']:
            Discipline.objects.create(title=d['title'], prof_type=d['prof_type'],
            constraints=ConstraintCollection.objects.first())
            #discipline.constraints = ConstraintCollection.objects.first()#############

def Set_Teachers():
    with codecs.open(path, 'r', 'utf_8_sig') as f:
        data = json.loads(f.read())
        for d in data['Teacher']:
            teacher = Teacher.objects.create(first_name=d['first_name'], last_name=d['last_name'],
             middle_name=d['middle_name'], constraints=json.dumps(d['constraints']), total_hours=d['total_hours'])
            teacher.disciplines.add(Discipline.objects.first())#Need's to be discussed

def Set_TrainingDirections():
    with codecs.open(path, 'r', 'utf_8_sig') as f:
        data = json.loads(f.read())
        for d in data['TrainingDirection']:
            TrainingDirection.objects.create(code=d['code'], name=d['name'],
             type=d['type'], constraints=d['constraints'])### constraints???

def Set_Flows():
    with codecs.open(path, 'r', 'utf_8_sig') as f:
        data = json.loads(f.read())
        for d in data['Flow']:
            Flow.objects.create(name=d['name'])

def Set_Groups():
    with codecs.open(path, 'r', 'utf_8_sig') as f:
        data = json.loads(f.read())
        for d in data['Group']:
            Group.objects.create(code=d['code'], count_of_students=d['count_of_students'],
             constraints=d['constraints'], flow=Flow.objects.first())
            #group.flow = Flow.objects.first()#### Foreign key in a cycle??

def Set_EducationPlans():
    with codecs.open(path, 'r', 'utf_8_sig') as f:
        data = json.loads(f.read())
        for d in data['EducationPlan']:
            EducationPlan.objects.create(type=d['type'], hours=d['hours'],
             constraints=d['constraints'], discipline=Discipline.objects.first(), group=Group.objects.first())
            #educationPlan.discipline = Discipline.objects.first()#### Foreign key in a cycle??
            #educationPlan.group = Group.objects.first()#### Foreign key in a cycle??

def Set_LectureHalls():
    with codecs.open(path, 'r', 'utf_8_sig') as f:
        data = json.loads(f.read())
        for d in data['LectureHall']:
            LectureHall.objects.create(spaciousness=d['spaciousness'], code=d['code'],
             building=d['building'], prof_type=d['prof_type'],
             constraints=ConstraintCollection.objects.first())
            #lechall.constraints = ConstraintCollection.objects.first()

def Test():
    print(ConstraintCollection.objects.all())

Main()
ConstraintCollection.objects.all()
