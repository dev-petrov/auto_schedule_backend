from index.tests import MainTest


class TestDiscipline(MainTest):

    url = '/api/lecture_hall/'

    def setUp(self):
        super().setUp()
        

    def test_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)


    def test_get(self):
        response = self.client.get(f'{self.url}{self.lecture_hall.id}/')
        data = {
            'id': self.lecture_hall.id, 
            'constraints': {
                'id': 1, 
                'projector': True, 
                'big_blackboard': True
            }, 
            'spaciousness': 20, 
            'code': 'Н301', 
            'building': 'E', 
            'prof_type': 'S'
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)


    def test_create(self):
        data = {
            'spaciousness': 40, 
            'building': 'V',
            'prof_type': 'S',
            'code': 'ПК404',
            'has_projector': True,
            'has_big_blackboard': True,
        }
        response = self.client.post(self.url, data, format='json')
        data = {
            'id': response.json()['id'], 
            'constraints': {
                'id': 1, 
                'projector': True, 
                'big_blackboard': True
            }, 
            'spaciousness': 40,
            'code': 'ПК404', 
            'building': 'V', 
            'prof_type': 'S'
        }
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), data)


    def test_update(self):
        data = {
            'spaciousness': 10, 
            'building': 'E',
            'prof_type': 'C',
            'code': 'Н301',
            'has_projector': True,
            'has_big_blackboard': False,
        }
        response = self.client.put(f'{self.url}{self.lecture_hall.id}/', data, format='json')
        data = {
            'id': self.lecture_hall.id, 
            'constraints': {
                'id': 2, 
                'projector': True, 
                'big_blackboard': False
            }, 
            'spaciousness': 10, 
            'code': 'Н301', 
            'building': 'E', 
            'prof_type': 'C'
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)


    def test_delete(self):
        response = self.client.delete(f'{self.url}{self.lecture_hall.id}/')
        self.assertEqual(response.status_code, 204)
