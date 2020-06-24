from index.tests import MainTest


class TestTrainingDirection(MainTest):

    url = '/api/training_direction/'

    def setUp(self):
        super().setUp()
        

    def test_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)


    def test_get(self):
        response = self.client.get(f'{self.url}{self.training_direction.id}/')
        data = {
            'id': self.training_direction.id, 
            'constraints': '{"buildings": ["E", "A", "P", "V", "S"], "day_constraints": {"1": [true, true, true, true, true, true, true], "2": [true, true, true, true, true, true, true], "3": [true, true, true, true, true, true, true], "4": [true, true, true, true, true, true, true], "5": [true, true, true, true, true, true, true], "6": [true, true, true, true, true, true, true]}}', 
            'code': 'test', 
            'name': 'Test', 
            'type': 'B'
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)


    def test_create(self):
        data = {
            'code': 'test3', 
            'name': 'Test3', 
            'type': 'M',
        }
        response = self.client.post(self.url, data, format='json')

        data = {
            'id': response.json()['id'], 
            'constraints': '{"buildings": ["E", "A", "P", "V", "S"], "day_constraints": {"1": [true, true, true, true, true, true, true], "2": [true, true, true, true, true, true, true], "3": [true, true, true, true, true, true, true], "4": [true, true, true, true, true, true, true], "5": [true, true, true, true, true, true, true], "6": [true, true, true, true, true, true, true]}}', 
            'code': 'test3', 
            'name': 'Test3', 
            'type': 'M'
        }
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), data)


    def test_update(self):
        data = {
            'code': 'test3', 
            'name': 'Test', 
            'type': 'S',

        }
        response = self.client.put(f'{self.url}{self.teacher.id}/', data, format='json')
        data = {
            'id': self.training_direction.id, 
            'constraints': '{"buildings": ["E", "A", "P", "V", "S"], "day_constraints": {"1": [true, true, true, true, true, true, true], "2": [true, true, true, true, true, true, true], "3": [true, true, true, true, true, true, true], "4": [true, true, true, true, true, true, true], "5": [true, true, true, true, true, true, true], "6": [true, true, true, true, true, true, true]}}', 
            'code': 'test3', 
            'name': 'Test', 
            'type': 'S'
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)


    # def test_delete(self):
    #     response = self.client.delete(f'{self.url}{self.lecture_hall.id}/')
    #     self.assertEqual(response.status_code, 204)
