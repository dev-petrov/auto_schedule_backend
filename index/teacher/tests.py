from index.tests import MainTest


class TestTeacher(MainTest):

    url = '/api/teacher/'

    def setUp(self):
        super().setUp()
        

    def test_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)


    def test_get(self):
        response = self.client.get(f'{self.url}{self.teacher.id}/')
        data = {
            'id': self.teacher.id,
            'first_name': 'Test', 
            'last_name': 'Testov', 
            'middle_name': 'Testovic', 
            'disciplines': [
                {
                    'id': self.discipline.id, 
                    'title': 'Дисциплина1',
                    'prof_type': 'S',
                    'type': 'L',
                }, 
                {
                    'id': self.discipline2.id, 
                    'title': 'Дисциплина2',
                    'prof_type': 'S',
                    'type': 'L',
                }
            ], 
            'constraints': '{"buildings_priority": ["E", "A", "V", "S", "P"], "day_constraints": {"1": [true, true, true, true, true, true, true], "2": [true, true, true, true, true, true, true], "3": [true, true, true, true, true, true, true], "4": [true, true, true, true, true, true, true], "5": [true, true, true, true, true, true, true], "6": [true, true, true, true, true, true, true]}}', 
            'total_hours': 180
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)


    def test_create(self):
        data = {
            'first_name': 'Tost', 
            'last_name': 'Tostov', 
            'middle_name': 'Tostovic', 
            'total_hours': 200,
            'disciplines_ids': [self.discipline2.id],

        }
        response = self.client.post(self.url, data, format='json')
        data = {
            'id': response.json()['id'], 
            'first_name': 'Tost', 
            'last_name': 'Tostov', 
            'middle_name': 'Tostovic', 
            'disciplines': [
                {
                    'id': self.discipline2.id,
                    'title': 'Дисциплина2',
                    'prof_type': 'S',
                    'type': 'L',
                }
            ], 
            'constraints': '{"buildings_priority": ["E", "A", "V", "S", "P"], "day_constraints": {"1": [true, true, true, true, true, true, true], "2": [true, true, true, true, true, true, true], "3": [true, true, true, true, true, true, true], "4": [true, true, true, true, true, true, true], "5": [true, true, true, true, true, true, true], "6": [true, true, true, true, true, true, true]}}', 
            'total_hours': 200
        }
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), data)


    def test_update(self):
        data = {
            'first_name': 'Test', 
            'last_name': 'Testov', 
            'middle_name': 'Testovic', 
            'total_hours': 190,
            'disciplines_ids': [self.discipline2.id],

        }
        response = self.client.put(f'{self.url}{self.teacher.id}/', data, format='json')
        data = {
            'id': self.teacher.id, 
            'first_name': 'Test', 
            'last_name': 'Testov', 
            'middle_name': 'Testovic', 
            'disciplines': [
                {
                    'id': self.discipline2.id, 
                    'title': 'Дисциплина2',
                    'prof_type': 'S',
                    'type': 'L',
                }
            ], 
            'constraints': '{"buildings_priority": ["E", "A", "V", "S", "P"], "day_constraints": {"1": [true, true, true, true, true, true, true], "2": [true, true, true, true, true, true, true], "3": [true, true, true, true, true, true, true], "4": [true, true, true, true, true, true, true], "5": [true, true, true, true, true, true, true], "6": [true, true, true, true, true, true, true]}}', 
            'total_hours': 190
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)


    # def test_delete(self):
    #     response = self.client.delete(f'{self.url}{self.lecture_hall.id}/')
    #     self.assertEqual(response.status_code, 204)
