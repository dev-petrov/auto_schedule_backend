from index.tests import MainTest


class TestEducationPlan(MainTest):

    url = '/api/education_plan/'

    def setUp(self):
        super().setUp()
        


    def test_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)


    def test_get(self):
        response = self.client.get(f'{self.url}{self.education_plan.id}/')
        data = {
            'id': self.education_plan.id, 
            'discipline': {
                'id': self.discipline.id, 
                'title': 'Дисциплина1',
                'prof_type': 'S',
                'type': 'L',
            }, 
            'group': {
                'id': self.group.id, 
                'code': '181-351'
            },
            'hours': 20, 
            'constraints': None
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)


    def test_create(self):
        data = {
            'discipline_id': self.discipline2.id, 
            'group_id': self.group2.id,
            'hours': 30,
        }
        response = self.client.post(self.url, data, format='json')
        data = {
            'id': response.json()['id'], 
            'discipline': {
                'id': self.discipline2.id, 
                'title': 'Дисциплина2',
                'prof_type': 'S',
                'type': 'L',
            }, 
            'group': {
                'id': self.group2.id, 
                'code': '181-352'
            },
            'hours': 30, 
            'constraints': None
        }
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), data)


    def test_update(self):
        data = {
            'discipline_id': self.discipline2.id, 
            'group_id': self.group.id,
            'hours': 30,
        }
        response = self.client.put(f'{self.url}{self.education_plan.id}/', data, format='json')
        data = {
            'id': self.education_plan.id, 
            'discipline': {
                'id': self.discipline2.id, 
                'title': 'Дисциплина2',
                'prof_type': 'S',
                'type': 'L',
            }, 
            'group': {
                'id': self.group.id, 
                'code': '181-351'
            },  
            'hours': 30, 
            'constraints': None
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)


    def test_delete(self):
        response = self.client.delete(f'{self.url}{self.education_plan.id}/')
        self.assertEqual(response.status_code, 204)
