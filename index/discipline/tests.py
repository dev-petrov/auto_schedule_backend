from index.tests import MainTest
from index.models import Discipline


class TestDiscipline(MainTest):
    def setUp(self):
        super().setUp()
        Discipline.objects.create()


    def test_get_list(self):
        pass

