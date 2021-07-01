import numpy as np
from algo.utils import prepare_data
import pandas as pd

MAX_LESSONS_IN_DAY = 5 # максимальное количество пар в день
GROUP_LESSONS = True # группируем пары с одинаковыми дисциплинами

class AlgoV2:
    def __init__(self):
        data = prepare_data()
        self.lessons = pd.DataFrame(columns=['discipline_id', 'group_id', 'teacher_id', 'lecture_hall_id', 'lesson', 'day_of_week'])
        self.disciplines = data['disciplines']
        self.teachers = pd.DataFrame(data['teachers'])
        self.groups = pd.DataFrame(data=data['groups'])
        self.lecture_halls = pd.DataFrame(data['lecture_halls'])

        self.teachers_disciplines = pd.DataFrame(columns=['teacher', 'discipline'])

        for _, teacher in self.teachers.iterrows():
            df = pd.DataFrame(columns=['discipline'], data=teacher['disciplines'])
            df['teacher'] = teacher['id']
            self.teachers_disciplines = self.teachers_disciplines.append(df)
        
    def _get_teacher(self, discipline, count_of_lessons):
        available_teachers = self.teachers_disciplines.loc[self.teachers_disciplines.discipline==discipline, 'teacher']
        teachers = self.teachers.loc[
            (self.teachers.id.isin(available_teachers)) & (self.teachers.total_hours >= count_of_lessons)
        ].sort_values(
            by=['total_hours', 'count_of_disciplines'], 
            ascending=[False, True],
        )
        if (len(teachers) == 0):
            return None
        return teachers.iloc[0]
    
    def _update_constraints(self, lessons, group, teacher):
        g_constraints = group.constraints.copy()
        t_constraints = teacher.constraints.copy()
        for day, lesson in lessons:
            g_constraints.append({'lesson': lesson, 'day_of_week': day})
            t_constraints.append({'lesson': lesson, 'day_of_week': day})
        
        g_constraints_arr = np.empty(1, dtype=object)
        g_constraints_arr[0] = g_constraints
        t_constraints_arr = np.empty(1, dtype=object)
        t_constraints_arr[0] = t_constraints

        self.groups.loc[self.groups.id==group.id, 'constraints'] = g_constraints_arr
        self.teachers.loc[self.teachers.id==teacher.id, 'constraints'] = t_constraints_arr

    def _get_lesson_time(self, teacher, group, count_of_lessons):
        INIT_DAYS = {
            1: [True, True, True, True, True, True, True,],
            2: [True, True, True, True, True, True, True,],
            3: [True, True, True, True, True, True, True,],
            4: [True, True, True, True, True, True, True,],
            5: [True, True, True, True, True, True, True,],
            6: [True, True, True, True, True, True, True,],
        }
        group_constraints = group.constraints
        teacher_constraints = teacher.constraints
        for les in group_constraints:
            INIT_DAYS[les['day_of_week']][les['lesson'] - 1] = False

        for les in teacher_constraints:
            INIT_DAYS[les['day_of_week']][les['lesson'] - 1] = False

        count_by_days_df = self.lessons.copy()
        count_by_days_df['cnt'] = 1
        count_by_days_df = count_by_days_df.loc[count_by_days_df.group_id==group.id, ['day_of_week', 'cnt']].set_index('day_of_week')
        count_by_days_df = count_by_days_df.count()

        for (day, cnt) in count_by_days_df.iteritems():
            if cnt >= MAX_LESSONS_IN_DAY:
                INIT_DAYS.pop(day, None)

        search_pattern = [
            True
            for _ in range(count_of_lessons)
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
                    self._update_constraints(lessons, group, teacher)
                    return lessons
                else:
                    self._update_constraints(ideal_lessons, group, teacher)
                    return ideal_lessons
            self._update_constraints(ideal_lessons, group, teacher)
            return lessons
        elif day != 0:
            self._update_constraints(ideal_lessons, group, teacher)
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
            self._update_constraints(lessons, group, teacher)
            return lessons
        else:
            return ((0, 0),)         

    def _get_lecture_hall(self, day, lesson, group, discipline):
        # tmp for test
        l_halls = self.lecture_halls.copy()
        l_halls['ordering'] = 999
        for constraint in group.building_constraints:
            l_halls.loc[l_halls.building==constraint['building'], 'ordering'] = constraint['ordering']
        l_halls.drop(index=l_halls[l_halls.ordering==999].index, inplace=True)
        not_avalable = self.lessons.loc[(self.lessons.day_of_week==day)&(self.lessons.lesson==lesson)&-(pd.isna(self.lessons.lecture_hall_id)), 'lecture_hall_id'].astype('int64')
        return l_halls[-l_halls.id.isin(not_avalable)].sort_values(by='ordering').iloc[0]

    def create_schedule(self):
        for _, group in self.groups.sort_values(
            by=['total_hours'], 
            ascending=[False],
        ).iterrows():
            for discipline in group.disciplines:
                teacher = self._get_teacher(discipline=discipline['discipline'], count_of_lessons=discipline['lessons_in_week'])
                if teacher is None:
                    print(f"No teacher {discipline['discipline']} lessons {discipline['lessons_in_week']}")
                    return []
                for i in range(discipline['lessons_in_week']):
                    self.lessons = self.lessons.append({"discipline_id": discipline['discipline'], "group_id": group.id, "teacher_id": teacher.id}, ignore_index=True)
        self.lessons = self.lessons.astype({'discipline_id': 'int64', 'group_id': 'int64', 'teacher_id': 'int64'})
        exclude_index = []
        for i, lesson in self.lessons.iterrows():
            group = self.groups[self.groups.id==lesson.group_id].iloc[0]
            teacher = self.teachers[self.teachers.id==lesson.teacher_id].iloc[0]
            if GROUP_LESSONS:
                if i in exclude_index:
                    continue
                lessons = self.lessons.loc[(self.lessons.group_id==group.id)&(self.lessons.teacher_id==teacher.id)&(self.lessons.discipline_id==lesson.discipline_id)]
                indexes = lessons.index
                times = self._get_lesson_time(teacher, group, len(indexes))
                exclude_index.extend(indexes)
            else:
                indexes = [i,]
                times = self._get_lesson_time(teacher, group, 1)
            if times[0] == (0, 0):
                print(f'No time for {group.code} with teacher {teacher.last_name} and discipline {lesson.discipline_id}')
                return []
            for index, i in enumerate(indexes):
                self.lessons.loc[i, ['day_of_week', 'lesson']] = times[index]
        self.lessons = self.lessons.astype({'day_of_week': 'int64', 'lesson': 'int64'})
        for i, lesson in self.lessons.iterrows():
            group = self.groups[self.groups.id==lesson.group_id].iloc[0]
            lecture_hall = self._get_lecture_hall(lesson.day_of_week, lesson.lesson, group, None)
            self.lessons.loc[i, 'lecture_hall_id'] = lecture_hall.id

        return self.lessons
