from rest_framework.test import APITestCase
from index.models import Discipline, ConstraintCollection



class MainTest(APITestCase):
    def setUp(self):
        super().setUp()
        constraints = list(ConstraintCollection.objects.all())
        self.discipline = Discipline.objects.create(
            title='Дисциплина1',
            constraints=constraints[1],
        )
        Discipline.objects.create(
            title='Дисциплина2',
            constraints=constraints[0],
        )
        Discipline.objects.create(
            title='Дисциплина3',
            constraints=constraints[3],
        )