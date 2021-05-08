from index.models import *
import json
import random
import codecs
from index.models import ConstraintCollection
from django.contrib.auth.models import User
from django.db import transaction
from algo.algov1 import Algorythm
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

def main():
    with transaction.atomic():
        set_disciplines()
        set_buildings()
        set_teachers()
        set_training_directions()
        set_flows()
        set_groups()
        set_education_plans()
        set_lecture_halls()
        set_lessons()
        User.objects.create_superuser('admin', email='admin@easytable.site', password='1234')
        print('Admin login: admin; admin pass: 1234')

def set_buildings():
    with codecs.open(path, 'r', 'utf_8_sig') as f:
        data = json.loads(f.read())
        for d in data['Building']:
            Building.objects.create(
                name=d['name'],
                code=d['code'],
                primary_color=d['primary_color'],
                secondary_color=d['secondary_color'],
            )

def set_disciplines():
    with codecs.open(path, 'r', 'utf_8_sig') as f:
        data = json.loads(f.read())
        for d in data['Discipline']:
            Discipline.objects.create(title=d['title'], type=d['type'], prof_type=d['prof_type'],
            constraints_id=random.randint(1,4), short_name=d['short_name'])


def set_teachers():
    with codecs.open(path, 'r', 'utf_8_sig') as f:
        data = json.loads(f.read())
        for d in data['Teacher']:
            teacher = Teacher.objects.create(first_name=d['first_name'], last_name=d['last_name'],
             middle_name=d['middle_name'], total_hours=d['total_hours'])
            for day, constraints in d['constraints']['day_constraints'].items():
                for i, available in enumerate(constraints):
                    if available:
                        TeacherLessonConstraint.objects.create(
                            lesson=i + 1,
                            day_of_week=day,
                            teacher=teacher,
                        )
            for dis in d['disciplines']:
                TeacherDetails.objects.create(teacher=teacher, discipline=Discipline.objects.filter(title=dis).first())


def set_training_directions():
    with codecs.open(path, 'r', 'utf_8_sig') as f:
        data = json.loads(f.read())
        for d in data['TrainingDirection']:
            t_direction = TrainingDirection.objects.create(
                code=d['code'], 
                name=d['name'],
                type=d['type'],
            )
            for day, constraints in d['constraints']['day_constraints'].items():
                for i, available in enumerate(constraints):
                    if available:
                        LessonTrainingDirectionConstraint.objects.create(
                            lesson=i + 1,
                            day_of_week=day,
                            training_direction=t_direction,
                        )
            for i, building_code in enumerate(d['constraints']['buildings']):
                BuildingTrainingDirectionConstraint.objects.create(
                    training_direction=t_direction,
                    ordering=i,
                    building=Building.objects.get(code=building_code),
                )

def set_flows():
    with codecs.open(path, 'r', 'utf_8_sig') as f:
        data = json.loads(f.read())
        for d in data['Flow']:
            Flow.objects.create(name=d['name'])

def set_groups():
    with codecs.open(path, 'r', 'utf_8_sig') as f:
        data = json.loads(f.read())
        for d in data['Group']:
            Group.objects.create(code=d['code'], count_of_students=d['count_of_students'],
             flow=Flow.objects.filter(name=d['flow']).first(),
             training_direction=TrainingDirection.objects.filter(code=d['direct']).first())


def set_education_plans():
    disciplines = list(Discipline.objects.all())
    count_of_lessons = [1, 2]
    for group in Group.objects.all():
        for i in range(random.randint(3, 5)):
            discipline = disciplines[random.randint(0, len(disciplines) - 1)]
            EducationPlan.objects.update_or_create(
                discipline=discipline,
                group=group,
                defaults={
                    'lessons_in_week': count_of_lessons[random.randint(0, 1)],
                }
            )


def set_lecture_halls():
    with codecs.open(path, 'r', 'utf_8_sig') as f:
        data = json.loads(f.read())
        for d in data['LectureHall']:
            building = Building.objects.get(code=d['building'])
            LectureHall.objects.create(spaciousness=d['spaciousness'], code=d['code'],
             building=building, prof_type=d['prof_type'],
             constraints_id=random.randint(1,4))
            #lechall.constraints = ConstraintCollection.objects.first()


def set_lessons():
    a = Algorythm()
    schedule = a.create_schedule()
    Lesson.objects.bulk_create(
        Lesson(**row)
        for i, row in schedule.iterrows()
    )
    # education_plans = {}
    # lecture_halls = list(LectureHall.objects.all())
    # disciplines = {}
    # for discipline in Discipline.objects.all():
    #     disciplines[discipline.id] = [
    #         teacher
    #         for teacher in discipline.teachers.all()
    #     ]
    # for plan in list(EducationPlan.objects.all().select_related('group', 'discipline').order_by('group')):
    #     key = plan.group_id
    #     if key not in education_plans:
    #         education_plans[key] = []
    #     education_plans[key].append(
    #         {
    #             'plan':plan,
    #             'lessons_in_week': round(plan.hours / 17),
    #             'teacher': disciplines[plan.discipline_id][random.randint(0, len(disciplines[plan.discipline_id]) - 1)],
    #         }
    #     )
    # lessons = []
    # for group in Group.objects.all():
    #     education_plan = education_plans[group.id]
    #     total_lessons = sum([x['lessons_in_week'] for x in education_plan])
    #     days_to_study = random.randint(5, 6)
    #     lessons_in_day = total_lessons / days_to_study
    #     day = 1
    #     les = 1
    #     for plan in education_plan:
    #         for i in range(plan['lessons_in_week']):
    #             if day == days_to_study + 1:
    #                 break
    #             lesson_check = Lesson.objects.filter(
    #                 teacher=plan['teacher'],
    #                 day_of_week=day,
    #             )
    #             if lesson_check.filter(
    #                 lesson=les,
    #             ).exists():
    #                 les = lesson_check.order_by('lesson').last().lesson + 1
                
    #             Lesson.objects.create(
    #                 group=group,
    #                 teacher=plan['teacher'],
    #                 lesson=les,
    #                 day_of_week=day,
    #                 discipline_id=plan['plan'].id,
    #                 lecture_hall=lecture_halls[random.randint(0, len(lecture_halls) - 1)],
    #             )
    #             les += 1
    #             if (les > lessons_in_day):
    #                 day += 1
    #                 les = 1
    # Lesson.objects.bulk_create(lessons)
            
