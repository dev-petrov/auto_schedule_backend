from index.tests import MainTest


class TestDiscipline(MainTest):

    url = '/api/group/'

    def setUp(self):
        super().setUp()
        


    def test_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)


    def test_get(self):
        response = self.client.get(f'{self.url}{self.group.id}/')
        data = {
            'id': self.group.id, 
            'constraints': '{"MO": [true, true, true, true, true, true, true], "TU": [true, true, true, true, true, true, true], "WE": [true, true, true, true, true, true, true], "TH": [true, true, true, true, true, true, true], "FR": [true, true, true, true, true, true, true], "SA": [true, true, true, true, true, true, true]}', 
            'flow': {
                'id': self.flow.id, 
                'name': 'Test'
            }, 
            'training_direction': {
                'id': self.training_direction.id, 
                'constraints': '{"buildings": ["E", "A", "P", "V", "S"], "day_constraints": {"MO": [true, true, true, true, true, true, true], "TU": [true, true, true, true, true, true, true], "WE": [true, true, true, true, true, true, true], "TH": [true, true, true, true, true, true, true], "FR": [true, true, true, true, true, true, true], "SA": [true, true, true, true, true, true, true]}}', 
                'code': 'test', 
                'name': 'Test', 
                'type': 'B'
            }, 
            'code': '181-351', 
            'count_of_students': 20
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)


    def test_create(self):
        data = {
            'flow_id': self.flow.id, 
            'training_direction_id': self.training_direction.id,
            'count_of_students': 10,
            'code': '181-331',
        }
        response = self.client.post(self.url, data, format='json')
        data = {
            'id': response.json()['id'], 
            'flow': {
                'id': self.flow.id, 
                'name': 'Test'
            }, 
            'training_direction': {
                'id': self.training_direction.id, 
                'constraints': '{"buildings": ["E", "A", "P", "V", "S"], "day_constraints": {"MO": [true, true, true, true, true, true, true], "TU": [true, true, true, true, true, true, true], "WE": [true, true, true, true, true, true, true], "TH": [true, true, true, true, true, true, true], "FR": [true, true, true, true, true, true, true], "SA": [true, true, true, true, true, true, true]}}', 
                'code': 'test', 
                'name': 'Test', 
                'type': 'B'
            }, 
            'constraints': '{"MO": [true, true, true, true, true, true, true], "TU": [true, true, true, true, true, true, true], "WE": [true, true, true, true, true, true, true], "TH": [true, true, true, true, true, true, true], "FR": [true, true, true, true, true, true, true], "SA": [true, true, true, true, true, true, true]}', 
            'code': '181-331', 
            'count_of_students': 10
        }
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), data)


    def test_update(self):
        data = {
            'flow_id': self.flow2.id, 
            'training_direction_id': self.training_direction.id,
            'count_of_students': 10,
            'code': '181-361',
        }
        response = self.client.put(f'{self.url}{self.group.id}/', data, format='json')
        data = {
            'id': self.group.id, 
            'flow': {
                'id': self.flow2.id, 
                'name': 'Test2'
            }, 
            'training_direction': {
                'id': self.training_direction.id, 
                'constraints': '{"buildings": ["E", "A", "P", "V", "S"], "day_constraints": {"MO": [true, true, true, true, true, true, true], "TU": [true, true, true, true, true, true, true], "WE": [true, true, true, true, true, true, true], "TH": [true, true, true, true, true, true, true], "FR": [true, true, true, true, true, true, true], "SA": [true, true, true, true, true, true, true]}}', 
                'code': 'test', 
                'name': 'Test', 
                'type': 'B'
            }, 
            'constraints': '{"MO": [true, true, true, true, true, true, true], "TU": [true, true, true, true, true, true, true], "WE": [true, true, true, true, true, true, true], "TH": [true, true, true, true, true, true, true], "FR": [true, true, true, true, true, true, true], "SA": [true, true, true, true, true, true, true]}', 
            'code': '181-361', 
            'count_of_students': 10
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)


    # def test_delete(self):
    #     response = self.client.delete(f'{self.url}{self.discipline.id}/')
    #     self.assertEqual(response.status_code, 204)
