from rest_framework.test import APITestCase
from index.models import (
    Discipline, 
    ConstraintCollection, 
    Group, 
    TrainingDirection,
    EducationPlan,
    Flow,
    LectureHall,
    Teacher,
    TeacherDetails,
) 



class MainTest(APITestCase):
    def setUp(self):
        super().setUp()
        constraints = list(ConstraintCollection.objects.all())
        self.discipline = Discipline.objects.create(
            title='Дисциплина1',
            constraints=constraints[1],
        )
        self.discipline2 = Discipline.objects.create(
            title='Дисциплина2',
            constraints=constraints[0],
        )
        Discipline.objects.create(
            title='Дисциплина3',
            constraints=constraints[3],
        )
        self.flow = Flow.objects.create(
            name='Test',
        )
        self.flow2 = Flow.objects.create(
            name='Test2',
        )
        self.training_direction = TrainingDirection.objects.create(
            code='test',
            name='Test',
        )
        self.training_direction2 = TrainingDirection.objects.create(
            code='test2',
            name='Test2',
        )
        self.group = Group.objects.create(
            training_direction=self.training_direction,
            flow=self.flow,
            count_of_students=20,
            code='181-351',
        )
        self.group2 = Group.objects.create(
            training_direction=self.training_direction,
            flow=self.flow,
            count_of_students=30,
            code='181-352',
        )
        self.education_plan = EducationPlan.objects.create(
            discipline=self.discipline,
            group=self.group,
            hours=20,
        )
        self.education_plan2 = EducationPlan.objects.create(
            discipline=self.discipline2,
            group=self.group,
            hours=30,
        )
        self.education_plan3 = EducationPlan.objects.create(
            discipline=self.discipline,
            group=self.group2,
            hours=20,
        )
        self.lecture_hall = LectureHall.objects.create(
            spaciousness=20,
            code='Н301',
            constraints=constraints[0],
        )
        self.lecture_hall2 = LectureHall.objects.create(
            spaciousness=25,
            code='Н305',
            constraints=constraints[2],
        )

        self.teacher = Teacher.objects.create(
            first_name='Test',
            last_name='Testov',
            middle_name='Testovic',
            total_hours=180,
        )

        self.teacher2 = Teacher.objects.create(
            first_name='Testa',
            last_name='Testova',
            middle_name='Testovna',
            total_hours=120,
        )
        TeacherDetails.objects.create(
            teacher=self.teacher,
            discipline=self.discipline,
        )
        TeacherDetails.objects.create(
            teacher=self.teacher,
            discipline=self.discipline2,
        )
