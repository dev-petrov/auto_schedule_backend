from index.models import Group
from index.serializers import FlowSerializer
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from index.serializers import FlowSerializer
from django_filters.rest_framework import FilterSet, CharFilter, NumberFilter


class GroupSerializer(serializers.ModelSerializer):
    constraints = serializers.JSONField()
    flow = FlowSerializer()

    class Meta:
        model = Group
        fields = '__all__'


class GroupFilter(FilterSet):
    code = CharFilter(field_name='code', lookup_expr='icontains')
    min_count_of_students = NumberFilter(field_name='count_of_students', lookup_expr='gte')
    max_count_of_students = NumberFilter(field_name='count_of_students', lookup_expr='lte')
    flow = CharFilter(field_name='flow', lookup_expr='name__icontains')

    class Meta:
        model = Group
        fields = {
            'code':['exact'],
            'min_count_of_students': ['exact'],
            'max_count_of_students': ['exact'],
            'flow': ['exact'],
        }


class GroupViewSet(viewsets.ModelViewSet):
    '''
    GET: /api/group/
    :params
        code: string
        min_count_of_students: int
        max_count_of_students: int
        flow: flow_id

    :code
        200

    :returns
        [
            {
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
            ...
        ]

    GET: /api/group/1/
    
    :code
        200

    :returns
        {
            "id": 1,
            "constraints": "{'MO': [True, False, True, True, True, False, True], 'TU': [True, True, False, True, True, True, False], 'WE': [True, False, True, False, True, True, True], 'TH': [True, False, True, True, False, True, False], 'FR': [True, True, False, True, True, True, True], 'SA': [True, False, True, False, True, False, True]}",
            "flow": {
                "id": 2,
                "name": "Веб-разработка"
            },
            "code": "181-351",
            "count_of_students": 15,
            "training_direction": 1
        }

    POST: /api/group/
.................................................................................................
    :params
        code: string, required=True
        min_count_of_students: int, required=True
        max_count_of_students: int, required=True
        flow: flow_id, required=True
    
    :code
        201
    
    :returns
        /////////////////
        ??????????????????
        /////////////////


    PUT: /api/group/1/
    :params
        code: string, required=True
        min_count_of_students: int, required=True
        max_count_of_students: int, required=True
        flow: flow_id, required=True

    :code
        200
    
    :returns
        //////////////////
        ??????????????????
        //////////////////

    DELETE: /api/group/1/

    :code
        204

    '''
    queryset = Group.objects.all()  
    serializer_class = GroupSerializer
    filterset_class = GroupFilter 
