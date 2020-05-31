from index.models import TrainingDirection
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from django_filters.rest_framework import FilterSet, CharFilter


class TrainingDirectionSerializer(serializers.ModelSerializer):
    constraints = serializers.JSONField()

    class Meta:
        model = TrainingDirection
        fields = '__all__'


class TrainingDirectionFilter(FilterSet):
    code = CharFilter(field_name='code', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    
    class Meta:
        model = TrainingDirection
        fields = {
            'code':['exact'],
            'name': ['exact'],
            'type': ['exact', 'in'],
        }

        
class TrainingDirectionViewSet(viewsets.ModelViewSet):
    '''
    GET: /api/training_direction/
    :params
        code: string (номер направления)
        name: string (название напрвления)
        type:
            'B': Бакалавриат
            'S': Специалитет
            'M': Магистратура

    :code
        200

    :returns
        [
            {
                "id": 1,
                "constraints": "['E', 'A', 'P', 'S', 'V']",
                "code": "09.01.01",
                "name": "Прикладная информатика",
                "type": "B"
            },
            ...
        ]

    GET: /api/training_direction/1/
    
    :code
        200

    :returns
        {
            "id": 1,
            "constraints": "['E', 'A', 'P', 'S', 'V']",
            "code": "09.01.01",
            "name": "Прикладная информатика",
            "type": "B"
        }

    POST: /api/training_direction/

    :params
        constraints: JSON
        code: string (номер направления), required=True
        name: string (название напрвления), required=True
        type: (как в GET), required=True
    
    :code
        201
    
    :returns
        {
            "id": 7,
            "constraints": {},
            "code": "1",
            "name": "ss",
            "type": "B"
        }


    PUT: /api/training_direction/1/
    :params
        constraints: JSON
        code: string (номер направления), required=True
        name: string (название напрвления), required=True
        type:(как в GET), required=True

    :code
        200
    
    :returns
        {
            "id": 1,
            "constraints": {},
            "code": "1",
            "name": "qw",
            "type": "B"
        }

    DELETE: /api/training_direction/1/

    :code
        204

    '''
    queryset = TrainingDirection.objects.all()  
    serializer_class = TrainingDirectionSerializer 
    filterset_class = TrainingDirectionFilter