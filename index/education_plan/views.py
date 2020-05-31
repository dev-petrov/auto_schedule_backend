from index.models import EducationPlan
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from index.group.views import GroupSerializer
from index.discipline.views import DisciplineSerializer
from django_filters.rest_framework import FilterSet, CharFilter


class EducationPlanSerializer(serializers.ModelSerializer):
    discipline = DisciplineSerializer()
    group = GroupSerializer()


    class Meta:
        model = EducationPlan
        fields = '__all__'


class EducationPlanFilter(FilterSet):
    discipline = CharFilter(field_name='discipline', lookup_expr='title__icontains')
    group = CharFilter(field_name='group', lookup_expr='code__icontains')

    class Meta:
        model = EducationPlan
        fields = {
            'discipline':['exact'],
            'group': ['exact'],
        }

        
class EducationPlanViewSet(viewsets.ModelViewSet):
    '''
    GET: /api/education_plan/
    :params
        discipline: string (название дисциплины)
        group: string (номер группы)
        hours: int
        type:
            'L': Лекция
            'P': Практика
            'LB': Лаб. работа

    :code
        200

    :returns
        [
            {
                "id": 1,
                "discipline": {
                    "id": 9,
                    "constraints": {
                        "id": 1,
                        "projector": true,
                        "big_blackboard": true
                    },
                    "title": "Физика",
                    "prof_type": "S"
                },
                "group": {
                    "id": 1,
                    "constraints": "{'MO': [True, False, True, True, True, False, True], 'TU': [True, True, False, True, True, True, False], 'WE': [True, False, True, False, True, True, True], 'TH': [True, False, True, True, False, True, False], 'FR': [True, True, False, True, True, True, True], 'SA': [True, False, True, False, True, False, True]}",
                    "flow": {
                        "id": 2,
                        "name": "Веб-разработка"
                    },
                    "code": "181-351",
                    "count_of_students": 15,
                    "training_direction": 1
                },
                "type": "L",
                "hours": 20,
                "constraints": "[]"
            },
            ...
        ]

    GET: /api/education_plan/1/
    
    :code
        200

    :returns
        {
            "id": 1,
            "discipline": {
                "id": 9,
                "constraints": {
                    "id": 1,
                    "projector": true,
                    "big_blackboard": true
                },
                "title": "Физика",
                "prof_type": "S"
            },
            "group": {
                "id": 1,
                "constraints": "{'MO': [True, False, True, True, True, False, True], 'TU': [True, True, False, True, True, True, False], 'WE': [True, False, True, False, True, True, True], 'TH': [True, False, True, True, False, True, False], 'FR': [True, True, False, True, True, True, True], 'SA': [True, False, True, False, True, False, True]}",
                "flow": {
                    "id": 2,
                    "name": "Веб-разработка"
                },
                "code": "181-351",
                "count_of_students": 15,
                "training_direction": 1
            },
            "type": "L",
            "hours": 20,
            "constraints": "[]"
        }

    POST: /api/education_plan/
    :params
        discipline: discipline_id, required=True
        group: group_id, required=True
        type: (как GET), required=True
        hours: int, required=True

    
    :code
        201
    
    :returns
        //////////////////////////
        ??????????????????
        //////////////////////////


    PUT: /api/education_plan/1/
    :params
        discipline: discipline_id, required=True
        group: group_id, required=True
        type: (как GET), required=True
        hours: int, required=True

    :code
        200
    
    :returns
        /////////////////
        ??????????????????
        /////////////////

    DELETE: /api/education_plan/1/

    :code
        204

    '''
    queryset = EducationPlan.objects.all()
    serializer_class = EducationPlanSerializer
    filterset_class = EducationPlanFilter