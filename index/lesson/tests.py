from index.tests import MainTest
from index.models import Lesson

class TestLesson(MainTest):

    url = '/api/lesson/'

    def setUp(self):
        super().setUp()
        self.lesson = Lesson.objects.create(
            discipline=self.discipline,
            group=self.group,
            teacher=self.teacher,
            lecture_hall=self.lecture_hall,
            lesson=1,
            day_of_week=1,
        )
        Lesson.objects.create(
            discipline=self.discipline,
            group=self.group,
            teacher=self.teacher,
            lecture_hall=self.lecture_hall,
            lesson=2,
            day_of_week=1,
        )
        

    def test_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)


    def test_get(self):
        response = self.client.get(f'{self.url}{self.lesson.id}/')
        data = {
            'id': self.lesson.id, 
            'discipline': {
                'id': self.discipline.id, 
                'prof_type': 'S', 
                'title': 'Дисциплина1', 
                'type': 'L'
            },
            'group': {
                'id': self.group.id, 
                'code': '181-351'
            }, 
            'teacher': {
                'id': self.teacher.id, 
                'first_name': 'Test', 
                'last_name': 'Testov', 
                'middle_name': 'Testovic'
            }, 
            'lecture_hall': {
                'id': self.lecture_hall.id, 
                'code': 'Н301', 
                'building': 'E', 
                'prof_type': 'S'
            }, 
            'lesson': 1, 
            'day_of_week': 1
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)


    def test_create(self):
        data = {
            'discipline_id': self.education_plan.id,
            'group_id': self.group.id,
            'teacher_id': self.teacher.id,
            'lecture_hall_id': self.lecture_hall2.id,
            'lesson': 3,
            'day_of_week': 1,
        }
        response = self.client.post(self.url, data, format='json')
        data = {
            'id': response.json()['id'], 
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
            'teacher': {
                'id': self.teacher.id, 
                'first_name': 'Test', 
                'last_name': 'Testov', 
                'middle_name': 'Testovic'
            }, 
            'lecture_hall': {
                'id': self.lecture_hall2.id, 
                'code': 'Н305', 
                'building': 'E', 
                'prof_type': 'S'
            }, 
            'lesson': 3, 
            'day_of_week': 1
        }
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), data)


    def test_update(self):
        data = {
            'discipline_id': self.education_plan2.id,
            'group_id': self.group.id,
            'teacher_id': self.teacher.id,
            'lecture_hall_id': self.lecture_hall2.id,
            'lesson': 1,
            'day_of_week': 1,
        }
        response = self.client.put(f'{self.url}{self.lesson.id}/', data, format='json')
        data = {
            'id': self.lesson.id, 
            'discipline': {
                'id': self.discipline2.id, 
                'prof_type': 'S', 
                'title': 'Дисциплина2', 
                'type': 'L'
            },
            'group': {
                'id': self.group.id, 
                'code': '181-351'
            }, 
            'teacher': {
                'id': self.teacher.id, 
                'first_name': 'Test', 
                'last_name': 'Testov', 
                'middle_name': 'Testovic'
            }, 
            'lecture_hall': {
                'id': self.lecture_hall2.id, 
                'code': 'Н305', 
                'building': 'E', 
                'prof_type': 'S'
            }, 
            'lesson': 1, 
            'day_of_week': 1
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)


    def test_delete(self):
        response = self.client.delete(f'{self.url}{self.lesson.id}/')
        self.assertEqual(response.status_code, 204)
