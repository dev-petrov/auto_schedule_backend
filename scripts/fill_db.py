from index.models import *
import json
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

def Set_Diciplines():
    objs = [
        Discipline(title='Линейная алгебра', prof_type='S', need_projector=False, need_big_blackboard=True),
        Discipline(title='Иностранный язык', prof_type='S', need_projector=False, need_big_blackboard=True),
        Discipline(title='Безопасность жизнедеятельности', prof_type='S', need_projector=True, need_big_blackboard=False),
        Discipline(title='Программирование мобильных приложений', prof_type='C', need_projector=True, need_big_blackboard=False),
        Discipline(title='Теория вероятнотей', prof_type='S', need_projector=False, need_big_blackboard=True),
        Discipline(title='Аналитика информационной безопасности', prof_type='S', need_projector=True, need_big_blackboard=False),
        Discipline(title='Основы сетевых технологий', prof_type='C', need_projector=True, need_big_blackboard=False),
        Discipline(title='Веб-разработка', prof_type='C', need_projector=True, need_big_blackboard=False),
        Discipline(title='Физика', prof_type='S', need_projector=True, need_big_blackboard=True),
        Discipline(title='Сопротивление материалов', prof_type='S', need_projector=False, need_big_blackboard=True),
        Discipline(title='История исскувств', prof_type='S', need_projector=True, need_big_blackboard=False),
        Discipline(title='Современный дизайн', prof_type='D', need_projector=True, need_big_blackboard=False),
        Discipline(title='Работа на фрезеровочных станках', prof_type='M', need_projector=False, need_big_blackboard=False),
    ]

    Discipline.objects.bulk_create(objs)

def Set_Teachers():
    
    Teacher.objects.create(first_name='Васильев', last_name='', middle_name='', constrins=json.dumps(), total_hours=4)
    
