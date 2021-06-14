'''
Algorythm for auto scheduling.
Petrov Anton
Shimankov Kirill
'''

'''
TODO
    учитывать коэф человеко/предмета
    добавить проверку препода (окно в пару если нужно перемещаться между корпусами)

'''

import pandas as pd
from index.models import (
    Teacher, 
    Discipline, 
    Lesson, 
    LectureHall, 
    ConstraintCollection, 
    EducationPlan, 
    Group, 
    Flow,
    TeacherDetails,
)
from django.db.models import F, Q, Sum, Count, FloatField, Value
from django.db.models.functions import Coalesce, Cast, Least
import json


COUNT_OF_WEEKS = 18
MAX_LESSONS_IN_WEEK = 25
COMBINE_LECTIONS = True


class Algorythm():
    
    def __init__(self):
        def _parse_constraints(obj):
            constr = json.loads(obj['constraints'].replace('\'', '\"').replace('True', 'true').replace('False', 'false'))
            if 'day_constraints' in constr:
                obj.update(constr['day_constraints'])
                constr.pop('day_constraints')
            # if 'buildings' in obj:
            #     obj['buildings'] = json.loads(obj['buildings'].replace('\'', '\"'))
            obj.update(constr)
            obj.pop('constraints', None)
            return obj

        self.lessons = pd.DataFrame(columns=['discipline_id', 'group_id', 'teacher_id', 'lecture_hall_id', 'lesson', 'day_of_week'])
        self.teachers = pd.DataFrame(data=list(map(_parse_constraints, Teacher.objects.all().annotate(
            count_of_disciplines=Count('disciplines'),
        ).values())))
        self.education_plan = pd.DataFrame(data=EducationPlan.objects.all().annotate(
            week_hours=Sum(F('hours') / COUNT_OF_WEEKS),
        ).values())
        self.disciplines = pd.DataFrame(data=Discipline.objects.annotate(
            coeff=Value(0, output_field=FloatField()),
            teachers_count=Count('teachers'),
            week_hours=Sum(F('educationplan__hours') / COUNT_OF_WEEKS),
        ).values())
        self.groups = pd.DataFrame(data=list(map(_parse_constraints, Group.objects.annotate(
            week_hours=Sum(F('educationplan__hours') / COUNT_OF_WEEKS),
            constraints=F('training_direction__constraints')
        ).order_by('-week_hours').values())))
        self.lecture_halls = pd.DataFrame(data=LectureHall.objects.all().values())
        self.teacher_details = pd.DataFrame(data=TeacherDetails.objects.all().values())
        self._change_teacher_disc_coef(1, 0)
        self.constraints_collection = {
            ConstraintCollection.objects.get(projector=False, big_blackboard=False).id: list(ConstraintCollection.objects.all().values_list('id', flat=True)),
            ConstraintCollection.objects.get(projector=True, big_blackboard=False).id: list(ConstraintCollection.objects.filter(projector=True).values_list('id', flat=True)),
            ConstraintCollection.objects.get(projector=False, big_blackboard=True).id: list(ConstraintCollection.objects.filter(big_blackboard=True).values_list('id', flat=True)),
            ConstraintCollection.objects.get(projector=True, big_blackboard=True).id: list(ConstraintCollection.objects.filter(big_blackboard=True, projector=True).values_list('id', flat=True)),
        }


    def check_data(self):
        res = self._check_lecture_halls()
        if not res[0]:
            return (False, res[1])


    def _get_teacher(self, discipline_id, count_of_pairs, exclude_teachers=[]):
        '''
        Подумать как применить коэффициент человеко/преподавателя
        '''
        teachers_disciplines = self.teacher_details.loc[self.teacher_details.discipline_id==discipline_id, 'teacher_id']
        teachers = self.teachers.loc[
            (self.teachers.id.isin(teachers_disciplines)) & (self.teachers.total_hours >= count_of_pairs)
        ].loc[(-self.teachers.id.isin(exclude_teachers))].sort_values(
            by=['total_hours', 'count_of_disciplines'], 
            ascending=[False, True],
        )

        if (len(teachers) == 0):
            teachers = self.teachers.loc[
                (self.teachers.id.isin(teachers_disciplines))
            ].loc[(-self.teachers.id.isin(exclude_teachers))].sort_values(
                by=['total_hours', 'count_of_disciplines'], 
                ascending=[False, True],
            )
            if (len(teachers) == 0):
                return None
            return teachers.iloc[0]
        else:
            return teachers.iloc[0]
        # exclude_teachers = self.lessons.loc[(self.lessons.day_of_week==day_of_week) & (self.lessons.lesson==lesson), 'teacher'].unique()
        # count_of_pairs = self.lessons.groupby(['teacher']).size().sort_values()
        # exclude_teachers_by_lessons = count_of_pairs[count_of_pairs]
        # teacher = None


    def _choose_lesson_positions(self, teacher, group, count_of_lessons, exclude_lessons={}, consider_teacher_constraints=True):
        '''
        TODO применить ограничения препода
        TODO применить ограничения группы
        '''

        INIT_DAYS = {
            1: [True, True, True, True, True, True, True,],
            2: [True, True, True, True, True, True, True,],
            3: [True, True, True, True, True, True, True,],
            4: [True, True, True, True, True, True, True,],
            5: [True, True, True, True, True, True, True,],
            6: [True, True, True, True, True, True, True,],
        }
        group_lessons = self.lessons.loc[self.lessons.group_id==group.id]
        teacher_lessons = self.lessons.loc[self.lessons.teacher_id==teacher.id]
        for i, les in group_lessons.iterrows():
            INIT_DAYS[les.day_of_week][les.lesson - 1] = False

        for i, les in teacher_lessons.iterrows():
            INIT_DAYS[les.day_of_week][les.lesson - 1] = False

        for day, lesson in exclude_lessons:
            INIT_DAYS[day][lesson - 1] = False

        if not consider_teacher_constraints:
            print('Not concidered')

        if consider_teacher_constraints:
            for i in range(6):
                for index, val in enumerate(teacher[str(i+1)]):
                    if not val:
                        INIT_DAYS[i + 1][index] = False 


        for i in range(6):
            for index, val in enumerate(group[str(i+1)]):
                if not val:
                    INIT_DAYS[i + 1][index] = False 
        search_pattern = [
            True
            for i in range(count_of_lessons)
        ]
        lesson = 7
        day = 0
        # идеальное совпадение
        for k, v in INIT_DAYS.items():
            for i in range(7 - count_of_lessons):
                if v[i:count_of_lessons + i] == search_pattern:
                    if i + 1 < lesson:
                        lesson = i + 1
                        day = k
                    continue
        
        ideal_lessons = [
            (day, lesson + i)
            for i in range(count_of_lessons)
        ]
        # if day != 0:
        #     return [
        #         (day, lesson + i)
        #         for i in range(count_of_lessons)
        #     ]
        
        lessons = []
        lessons_amount = count_of_lessons
        prev_lesson = 0
        # пытаемся как можно больше пар рядом распределить
        for k, v in INIT_DAYS.items():
            if lessons_amount == 0:
                break
            for index, item in enumerate(v):
                if item and index == prev_lesson:
                    prev_lesson += 1
                    lessons_amount -= 1
                    lessons.append((k, index + 1))
                    if lessons_amount == 0:
                        break
                else:
                    prev_lesson = 0
                    break
        if len(lessons) == count_of_lessons:
            count_of_better_lessons = 0
            if day != 0:
                for day, less in lessons:
                    if less < lesson:
                        count_of_lessons += 1
                if count_of_better_lessons > 1:
                    return lesson
                else:
                    return ideal_lessons
            return lessons
        elif day != 0:
            return ideal_lessons
        
        lessons = []
        lessons_amount = count_of_lessons
        # распределение с окнами
        for k, v in INIT_DAYS.items():
            if lessons_amount == 0:
                break
            for index, item in enumerate(v):
                if item:
                    lessons_amount -= 1
                    lessons.append((k, index + 1))
                    if lessons_amount == 0:
                        break
        if len(lessons) == count_of_lessons:
            return lessons
        else:
            return ((0, 0),)                  
        


    def _choose_lecture_halls(self, group, teacher, lessons, discipline_id):
        '''
        добавить проверку препода (окно в пару если нужно перемещаться между корпусами)
        '''
        discipline = self.disciplines[self.disciplines.id==discipline_id].iloc[0]
        lessons_and_lecture_halls = []
        for day, lesson in lessons:
            exclude_lecture_halls = self.lessons.loc[(self.lessons.day_of_week==day) & (self.lessons.lesson==lesson), 'lecture_hall_id'].unique()
            lh_filter = -self.lecture_halls.id.isin(exclude_lecture_halls) & \
                (self.lecture_halls.spaciousness >= group.count_of_students) & \
                (self.lecture_halls.building.isin(group.buildings)) & \
                (self.lecture_halls.constraints_id.isin(self.constraints_collection[discipline.constraints_id])) 
            if discipline.prof_type != 'S':
                lh_filter &= (self.lecture_halls.prof_type==discipline.prof_type)
            lessons_in_day = self.lessons.loc[(self.lessons.group_id==group.id) & (self.lessons.day_of_week==day), 'lecture_hall_id']
            if len(lessons_in_day):
                lh_filter &= (self.lecture_halls.building==self.lecture_halls.loc[self.lecture_halls.id==lessons_in_day.iloc[0], 'building'].iloc[0])

            lecture_halls = self.lecture_halls.loc[lh_filter].sort_values(by='spaciousness',)
            if len(lecture_halls):
                lessons_and_lecture_halls.append((lecture_halls.iloc[0].id, day, lesson))
            else:
                # думаю, что стоит продолжить поиск и потом пару распределить
                lessons_and_lecture_halls.append((None, day, lesson))
        return lessons_and_lecture_halls

        # exclude_lecture_halls = self.lessons.loc[exclude_lh_cond, 'lecture_hall_id'].unique()
        # lecture_halls = self.lecture_halls[-self.lecture_halls.id.isin(exclude_lecture_halls) & self.lecture_halls.spaciousness >= group.count_of_students]
        


    def create_schedule(self):
        for _, group in self.groups.iterrows():
            education_plan = self.education_plan.loc[self.education_plan.group_id==group.id].sort_values(by='week_hours', ascending=False,)
            while len(education_plan.loc[education_plan.week_hours > 0]) != 0:
                discipline = education_plan.loc[education_plan.week_hours > 0].iloc[0]
                disc_hours = discipline.week_hours
                lesson_times = [(0, 0),]
                exclude_teachers = []
                consider_teacher_constraints = True
                while lesson_times[0][0] == 0: 
                    teacher = self._get_teacher(discipline.discipline_id, discipline.week_hours, exclude_teachers=exclude_teachers)
                    if teacher is None and consider_teacher_constraints:
                        consider_teacher_constraints = False
                        exclude_teachers = []
                    elif teacher is None:
                        print(self.lessons)
                        disc = Discipline.objects.get(id=discipline.discipline_id)
                        return f'Не хватает преподавателей для дисциплины {disc.title}'
                    lesson_times = self._choose_lesson_positions(teacher, group, discipline.week_hours, consider_teacher_constraints=consider_teacher_constraints)
                    exclude_teachers.append(teacher.id)
                exclude_lessons = []
                while discipline.week_hours != 0:
                    lecture_halls = self._choose_lecture_halls(group, teacher.id, lesson_times, discipline.discipline_id)
                    for lecture_hall, day_of_week, lesson in lecture_halls:
                        if lecture_hall:
                            self.lessons = self.lessons.append(
                                {
                                    'lecture_hall_id': lecture_hall,
                                    'group_id': group.id,
                                    'teacher_id': teacher.id,
                                    'discipline_id': discipline.discipline_id,
                                    'lesson': lesson,
                                    'day_of_week': day_of_week,
                                }, 
                                ignore_index=True
                            )
                            discipline.week_hours -= 1
                    exclude_lessons += lesson_times
                    lesson_times = self._choose_lesson_positions(teacher, group, discipline.week_hours, exclude_lessons=exclude_lessons)
                    if len(lesson_times) != 0 and lesson_times[0][0] == 0:
                        disc = Discipline.objects.get(id=discipline.discipline_id)
                        print(f'Не получается распределить пары по {disc.title}'
                        f' в количистве {discipline.week_hours} с преподавателем'
                        f' {teacher.first_name} {teacher.last_name}'
                        f' для группы {group.code}'
                        f' из-за нехватки аудиторий типа {disc.prof_type}')
                        break
                education_plan.at[discipline.name, :] = discipline
                self.teachers.at[teacher.name, 'total_hours'] -= disc_hours
                    
        print(self.lessons)
        return self.lessons

    def _change_teacher_disc_coef(self, discipline_id, count):
        def _update_coeff(obj):
            obj.coeff = (obj.week_hours) / obj.teachers_count
            return obj
        cond = self.disciplines.id==discipline_id
        self.disciplines.loc[cond, 'week_hours'] -= count
        del_cond = self.disciplines[self.disciplines.week_hours <= 0].index
        self.disciplines.drop(del_cond, inplace=True)
        self.disciplines = self.disciplines.apply(_update_coeff, axis=1)

   
    def _check_lecture_halls(self):
        ERROR_MESSAGES = {
            'simple':'Не хватает простых аудиторий в размере {} шт.',
            'comp': 'Не хватает компьютерных аудиторий в размере {} шт.',
            'design': 'Не хватает аудиторий для дизайнеров в размере {} шт.',
            'lab': 'Не хватает лабораторий в размере {} шт.',
            'mechanic': 'Не хватает аудиторий для механиков в размере {} шт.',
        }
        def _check_prof_type(error_list, key, l_halls, ed_plan):
            if key == 'simple':
                l_halls[key] = sum(l_halls.values())
            l_halls[key] = l_halls[key] - ed_plan[key]
            if l_halls[key] < 0:
                errors.append(ERROR_MESSAGES[key].format(l_halls[key] * -1))
                l_halls[key] = 0

        ed_plan = EducationPlan.objects.annotate(
            per_week=F('hours') / COUNT_OF_WEEKS,
        ).aggregate(
            comp=Coalesce(Sum('per_week', filter=Q(discipline__prof_type=Discipline.PROF_TYPE_COMP)), 0),
            design=Coalesce(Sum('per_week', filter=Q(discipline__prof_type=Discipline.PROF_TYPE_DESIGN)), 0),
            lab=Coalesce(Sum('per_week', filter=Q(discipline__prof_type=Discipline.PROF_TYPE_LAB)), 0),
            mechanic=Coalesce(Sum('per_week', filter=Q(discipline__prof_type=Discipline.PROF_TYPE_MECHANIC)), 0),
            simple=Coalesce(Sum('per_week', filter=Q(discipline__prof_type=Discipline.PROF_TYPE_SIMPLE)), 0),
        )
        l_halls = LectureHall.objects.aggregate(
            comp=Coalesce(Count('id', filter=Q(prof_type=Discipline.PROF_TYPE_COMP)), 0),
            design=Coalesce(Count('id', filter=Q(prof_type=Discipline.PROF_TYPE_DESIGN)), 0),
            lab=Coalesce(Count('id', filter=Q(prof_type=Discipline.PROF_TYPE_LAB)), 0),
            mechanic=Coalesce(Count('id', filter=Q(prof_type=Discipline.PROF_TYPE_MECHANIC)), 0),
            simple=Coalesce(Count('id', filter=Q(prof_type=Discipline.PROF_TYPE_SIMPLE)), 0),
        )
        errors = []
        
        for i in l_halls:
            _check_prof_type(errors, i, l_halls, ed_plan)
        
        if len(errors):
            return (False, errors)
        
        return (True, [])

    def check_teachers(self):
        # продумать проверку преподов
        return True



class Algo:
    def __init__(self):
        def _parse_constraints(obj):
            constr = json.loads(obj['constraints'].replace('\'', '\"').replace('True', 'true').replace('False', 'false'))
            if 'day_constraints' in constr:
                obj.update(constr['day_constraints'])
                constr.pop('day_constraints')
            # if 'buildings' in obj:
            #     obj['buildings'] = json.loads(obj['buildings'].replace('\'', '\"'))
            obj.update(constr)
            obj.pop('constraints', None)
            return obj

        self.lessons = pd.DataFrame(columns=['discipline_id', 'group_id', 'teacher_id', 'lecture_hall_id', 'lesson', 'day_of_week'])
        self.teachers_groups = pd.DataFrame(columns=['discipline_id', 'group_id', 'teacher_id', 'hours', 'flow_id', 'type'])
        self._pre_lessons = pd.DataFrame(columns=['discipline_id', 'group_id', 'teacher_id', 'flow_id', 'type', 'day_of_week', 'lesson'])
        self.teachers = pd.DataFrame(data=list(map(_parse_constraints, Teacher.objects.all().annotate(
            count_of_disciplines=Count('disciplines'),
            hours=Least(F('total_hours'), MAX_LESSONS_IN_WEEK, output_field=FloatField()),
        ).order_by('count_of_disciplines').values())))
        self.education_plan = pd.DataFrame(data=EducationPlan.objects.all().annotate(
            week_hours=F('hours') / COUNT_OF_WEEKS
        ).order_by('group_id', 'week_hours').values())
        self.disciplines = pd.DataFrame(data=Discipline.objects.annotate(
            week_hours=Sum(F('educationplan__hours') / COUNT_OF_WEEKS),
        ).values())
        self.groups = pd.DataFrame(data=list(map(_parse_constraints, Group.objects.annotate(
            week_hours=Sum(F('educationplan__hours') / COUNT_OF_WEEKS),
            constraints=F('training_direction__constraints')
        ).order_by('-week_hours').values())))
        self.lecture_halls = pd.DataFrame(data=LectureHall.objects.all().values())
        self.teacher_details = pd.DataFrame(data=TeacherDetails.objects.all().annotate(code=F('discipline__code')).values())
        self.constraints_collection = {
            ConstraintCollection.objects.get(projector=False, big_blackboard=False).id: list(ConstraintCollection.objects.all().values_list('id', flat=True)),
            ConstraintCollection.objects.get(projector=True, big_blackboard=False).id: list(ConstraintCollection.objects.filter(projector=True).values_list('id', flat=True)),
            ConstraintCollection.objects.get(projector=False, big_blackboard=True).id: list(ConstraintCollection.objects.filter(big_blackboard=True).values_list('id', flat=True)),
            ConstraintCollection.objects.get(projector=True, big_blackboard=True).id: list(ConstraintCollection.objects.filter(big_blackboard=True, projector=True).values_list('id', flat=True)),
        }

    
    def _get_teacher(self, discipline, group, count_of_pairs, exclude_teachers=[]):
        if COMBINE_LECTIONS and discipline.type == Discipline.TYPE_LECTION and group.flow_id != None:
            # groups = self.groups.loc[self.groups.flow_id=group.flow_id, 'id']
            teacher = self.teachers_groups.loc[(self.teachers_groups.flow_id==group.flow_id) & (self.teachers_groups.discipline_id==discipline.id),:]
            if (len(teacher) != 0):
                max_pairs = teacher.loc['hours'].max()
                if max_pairs < count_of_pairs:
                    self.teachers.at[teachers.iloc[0].id, 'total_hours'] -= count_of_pairs - max_pairs
                return teacher.loc['teeacher_id'].iloc[0]
        teachers_disciplines = self.teacher_details.loc[self.teacher_details.code==discipline.code, 'teacher_id']
        teachers = self.teachers.loc[
            (self.teachers.id.isin(teachers_disciplines)) & (self.teachers.hours >= count_of_pairs)
        ].loc[(-self.teachers.id.isin(exclude_teachers))].sort_values(
            by=['count_of_disciplines', 'hours'], 
            ascending=[True, False],
        )

        if (len(teachers) == 0):
            # teachers = self.teachers.loc[
            #     (self.teachers.id.isin(teachers_disciplines))
            # ].loc[(-self.teachers.id.isin(exclude_teachers))].sort_values(
            #     by=['count_of_disciplines', 'hours'], 
            #     ascending=[True, False],
            # )
            # if (len(teachers) == 0):
            #     return None
            # return teachers.iloc[0]
            print('No teachers')
            return None
        else:
            self.teachers.at[teachers.iloc[0].id, 'total_hours'] -= count_of_pairs
            return teachers.iloc[0]


    def _group_teachers_and_groups(self):
        for _, row in self.education_plan.iterrows():
            discipline = self.disciplines.loc[self.disciplines.id=row.discipline_id].iloc[0]
            group = self.groups.loc[self.groups.id=row.group_id].iloc[0]
            teacher = self._get_teacher(discipline, group, row.week_hours)
            if teacher == None:
                print(f'No teachers for {group.code} {discipline.title}')
            self.teachers_groups = self.teachers_groups.append(
                {
                    'group_id': group.id,
                    'teacher_id': teacher,
                    'discipline_id': discipline.id,
                    'flow_id': group.flow_id,
                    'hours': row.week_hours,
                    'type': discipline.type,
                }, 
                ignore_index=True
            )

    def _get_lesson_time(self, teacher, group, count_of_lessons, exclude_lessons={}, consider_teacher_constraints=True):
        INIT_DAYS = {
            1: [True, True, True, True, True, True, True,],
            2: [True, True, True, True, True, True, True,],
            3: [True, True, True, True, True, True, True,],
            4: [True, True, True, True, True, True, True,],
            5: [True, True, True, True, True, True, True,],
            6: [True, True, True, True, True, True, True,],
        }
        group_lessons = self.pre_lesson.loc[self.pre_lesson.group_id==group.id]
        teacher_lessons = self.pre_lesson.loc[self.pre_lesson.teacher_id==teacher.id]
        for i, les in group_lessons.iterrows():
            INIT_DAYS[les.day_of_week][les.lesson - 1] = False

        for i, les in teacher_lessons.iterrows():
            INIT_DAYS[les.day_of_week][les.lesson - 1] = False

        for day, lesson in exclude_lessons:
            INIT_DAYS[day][lesson - 1] = False

        if not consider_teacher_constraints:
            print('Not concidered')

        if consider_teacher_constraints:
            for i in range(6):
                for index, val in enumerate(teacher[str(i+1)]):
                    if not val:
                        INIT_DAYS[i + 1][index] = False 


        for i in range(6):
            for index, val in enumerate(group[str(i+1)]):
                if not val:
                    INIT_DAYS[i + 1][index] = False 
        search_pattern = [
            True
            for i in range(count_of_lessons)
        ]
        lesson = 7
        day = 0
        # идеальное совпадение
        for k, v in INIT_DAYS.items():
            for i in range(7 - count_of_lessons):
                if v[i:count_of_lessons + i] == search_pattern:
                    if i + 1 < lesson:
                        lesson = i + 1
                        day = k
                    continue
        
        ideal_lessons = [
            (day, lesson + i)
            for i in range(count_of_lessons)
        ]
        # if day != 0:
        #     return [
        #         (day, lesson + i)
        #         for i in range(count_of_lessons)
        #     ]
        
        lessons = []
        lessons_amount = count_of_lessons
        prev_lesson = 0
        # пытаемся как можно больше пар рядом распределить
        for k, v in INIT_DAYS.items():
            if lessons_amount == 0:
                break
            for index, item in enumerate(v):
                if item and index == prev_lesson:
                    prev_lesson += 1
                    lessons_amount -= 1
                    lessons.append((k, index + 1))
                    if lessons_amount == 0:
                        break
                else:
                    prev_lesson = 0
                    break
        if len(lessons) == count_of_lessons:
            count_of_better_lessons = 0
            if day != 0:
                for day, less in lessons:
                    if less < lesson:
                        count_of_lessons += 1
                if count_of_better_lessons > 1:
                    return lesson
                else:
                    return ideal_lessons
            return lessons
        elif day != 0:
            return ideal_lessons
        
        lessons = []
        lessons_amount = count_of_lessons
        # распределение с окнами
        for k, v in INIT_DAYS.items():
            if lessons_amount == 0:
                break
            for index, item in enumerate(v):
                if item:
                    lessons_amount -= 1
                    lessons.append((k, index + 1))
                    if lessons_amount == 0:
                        break
        if len(lessons) == count_of_lessons:
            return lessons
        else:
            return ((0, 0),)

    
    def _get_time_for_lection(self, teacher, group, discipline, count_of_lessons):
        '''
        #TODO не учитывается количество пар, если уже что-то распределено
        '''
        # groups = self.groups.loc[self.groups.flow_id=group.flow_id, 'id']
        lessons = self.prev_lesson.loc[(self.pre_lesson.flow_id==group.flow_id) & (self.pre_lesson.discipline_id==discipline.id),:]
        if (len(lessons) != 0):
            return [(row.day_of_week, row.lesson) for _, row in lessons.iterrows()]
        else:
            return self._get_lesson_time(teacher, group, count_of_lessons,)


    def _get_lecture_halls(self, group, teacher, lessons, discipline_id, prev_buliding=None):
        '''
        добавить проверку препода (окно в пару если нужно перемещаться между корпусами)
        '''
        discipline = self.disciplines[self.disciplines.id==discipline_id].iloc[0]
        lessons_and_lecture_halls = []
        for day, lesson in lessons:
            exclude_lecture_halls = self.lessons.loc[(self.lessons.day_of_week==day) & (self.lessons.lesson==lesson), 'lecture_hall_id'].unique()
            lh_filter = -self.lecture_halls.id.isin(exclude_lecture_halls) & \
                (self.lecture_halls.spaciousness >= group['count_of_students']) & \
                (self.lecture_halls.building.isin(group['buildings'])) & \
                (self.lecture_halls.constraints_id.isin(self.constraints_collection[discipline.constraints_id])) 
            if discipline.prof_type != 'S':
                lh_filter &= (self.lecture_halls.prof_type==discipline.prof_type)
            if prev_buliding:
                lh_filter &= (self.lecture_halls.building==prev_buliding)
            lessons_in_day = self.lessons.loc[(self.lessons.group_id==group.id) & (self.lessons.day_of_week==day), 'lecture_hall_id']
            if len(lessons_in_day):
                lh_filter &= (self.lecture_halls.building==self.lecture_halls.loc[self.lecture_halls.id==lessons_in_day.iloc[0], 'building'].iloc[0])

            lecture_halls = self.lecture_halls.loc[lh_filter].sort_values(by='spaciousness',)
            if len(lecture_halls):
                lessons_and_lecture_halls.append((lecture_halls.iloc[0].id, day, lesson))
            else:
                # думаю, что стоит продолжить поиск и потом пару распределить
                lessons_and_lecture_halls.append((None, day, lesson))
        return lessons_and_lecture_halls
    

    def _get_lecture_halls_for_lection(self, group, teacher, lessons, discipline):
        pass