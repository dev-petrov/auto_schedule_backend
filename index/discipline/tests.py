from index.tests import MainTest
from index.models import Discipline


class TestDiscipline(MainTest):

    url = '/api/discipline/'

    def setUp(self):
        super().setUp()
        


    def test_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)


    def test_get(self):
        response = self.client.get(f'{self.url}{self.discipline.id}/')
        data = {
            'id': self.discipline.id, 
            'constraints': {
                'id': 2, 
                'projector': True, 
                'big_blackboard': False
            }, 
            'title': 'Дисциплина1', 
            'prof_type': 'S',
            'type': 'L',
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)


    def test_create(self):
        data = {
            'title': 'Дисциплина4', 
            'prof_type': 'C',
            'need_projector': True,
            'need_big_blackboard': True,
        }
        response = self.client.post(self.url, data, format='json')
        data = {
            'id': response.json()['id'], 
            'constraints': {
                'id': 1, 
                'projector': True, 
                'big_blackboard': True
            }, 
            'title': 'Дисциплина4', 
            'prof_type': 'C',
            'type': 'L',
        }
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), data)


    def test_update(self):
        data = {
            'title': 'Дисциплина4', 
            'prof_type': 'C',
            'need_projector': False,
            'need_big_blackboard': True,
        }
        response = self.client.put(f'{self.url}{self.discipline.id}/', data, format='json')
        data = {
            'id': self.discipline.id, 
            'constraints': {
                'id': 3, 
                'projector': False, 
                'big_blackboard': True
            }, 
            'title': 'Дисциплина4', 
            'prof_type': 'C',
            'type': 'L',
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)


    # def test_delete(self):
    #     response = self.client.delete(f'{self.url}{self.discipline.id}/')
    #     self.assertEqual(response.status_code, 204)
