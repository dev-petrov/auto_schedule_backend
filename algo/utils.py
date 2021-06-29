from django.db.models import Sum
from index.models import (
    Teacher, 
    Discipline, 
    LectureHall, 
    EducationPlan, 
    Group, 
    TeacherDetails,
    TeacherLessonConstraint,
    LessonTrainingDirectionConstraint,
    BuildingTrainingDirectionConstraint,
)

def prepare_data():
    teachers = Teacher.objects.all()
    disciplines = Discipline.objects.all()
    lecture_halls = LectureHall.objects.all()
    groups = Group.objects.all()
    education_plans = EducationPlan.objects.all()
    total_lessons = EducationPlan.objects.values('group_id').annotate(
        lessons=Sum('lessons_in_week'),
    )
    teacher_details = TeacherDetails.objects.all()
    teacher_constraints  = TeacherLessonConstraint.objects.all()
    training_directions_lesson_constraints = LessonTrainingDirectionConstraint.objects.all()
    training_directions_building_constraints = BuildingTrainingDirectionConstraint.objects.all()

    groupped_education_plans = {}
    for plan in education_plans:
        groupped_education_plans.setdefault(plan.group_id, []).append(
            {
                'discipline': plan.discipline_id,
                'lessons_in_week': plan.lessons_in_week,
            }
        )

    groupped_teacher_details = {}
    for detail in teacher_details:
        groupped_teacher_details.setdefault(detail.teacher_id, []).append(
            detail.discipline_id
        )

    groupped_teacher_constraints = {}
    for constraint in teacher_constraints:
        groupped_teacher_constraints.setdefault(constraint.teacher_id, []).append(
            {
                'lesson': constraint.lesson,
                'day_of_week': constraint.day_of_week,
            }
        )

    groupped_training_directions_lesson_constraints = {}
    for constraint in training_directions_lesson_constraints:
        groupped_training_directions_lesson_constraints.setdefault(constraint.training_direction_id, []).append(
            {
                'lesson': constraint.lesson,
                'day_of_week': constraint.day_of_week,
            }
        )

    groupped_training_directions_building_constraints = {}
    for constraint in training_directions_building_constraints:
        groupped_training_directions_building_constraints.setdefault(constraint.training_direction_id, []).append(
            {
                'building': constraint.building_id,
                'ordering': constraint.ordering,
            }
        )

    groupped_total_lessons = {}
    for total in total_lessons:
        groupped_total_lessons[total['group_id']] = total['lessons']

    data = {
        'teachers': [
            {
                'id': t.id,
                'last_name': t.last_name,
                'total_hours': len(groupped_teacher_constraints.get(t.id, [])),
                'count_of_disciplines': len(groupped_teacher_details.get(t.id, [])),
                'constraints': groupped_teacher_constraints.get(t.id, []),
                'init_constraints': groupped_teacher_constraints.get(t.id, []),
                'disciplines': groupped_teacher_details.get(t.id, []),
            }
            for t in teachers
        ],
        'disciplines': {},
        'lecture_halls': [
            {
                'id': lecture_hall.id,
                'spaciousness': lecture_hall.spaciousness,
                'building': lecture_hall.building_id,
                'constraints': lecture_hall.constraints_id,
                'prof_type': lecture_hall.prof_type,
            }
            for lecture_hall in lecture_halls
        ],
        'groups': [
            {
                'id': g.id,
                'code': g.code,
                'total_hours': groupped_total_lessons.get(g.id, 0),
                'constraints': groupped_training_directions_lesson_constraints.get(g.training_direction_id, []),
                'init_constraints': groupped_training_directions_lesson_constraints.get(g.training_direction_id, []),
                'building_constraints': groupped_training_directions_building_constraints.get(g.training_direction_id, []),
                'disciplines': groupped_education_plans.get(g.id, []),
            }
            for g in groups
        ],
    }

    for discipline in disciplines:
        data['disciplines'][discipline.id] = {
            'title': discipline.title,
            'prof_type': discipline.prof_type,
            'constraints': discipline.constraints_id,
            'type': discipline.type,
        }
    
    return data
