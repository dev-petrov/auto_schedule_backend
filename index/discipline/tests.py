from index.tests import MainTest
from index.models import Discipline


class TestDiscipline(MainTest):

    url = '/api/discipline/'

    def setUp(self):
        super().setUp()
        


    def test_get_list(self):
        response = self.client.get(self.url)
        print(response.json())

