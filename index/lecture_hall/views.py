from index.models import LectureHall
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from index.serializers import ConstraintCollectionSerializer
from django_filters.rest_framework import FilterSet, CharFilter, NumberFilter


class LectureHallSerializer(serializers.ModelSerializer):
    constraints = ConstraintCollectionSerializer()

    class Meta:
        model = LectureHall
        fields = '__all__'

    def save(self, *args, **kwargs):
        has_projector = self.validated_data.pop('has_projector')
        has_blackboard = self.validated_data.pop('has_blackboard')
        constraints = ConstraintCollection.objects.get(
            projector=has_projector, 
            big_blackboard=has_blackboard
        )
        self.validated_data['constraints'] = constraints
        super(LectureHallSerializer, self).save(*args, **kwargs)


class LectureHallFilter(FilterSet):
    code = CharFilter(field_name='code', lookup_expr='icontains')
    min_spaciousness = NumberFilter(field_name='spaciousness', lookup_expr='gte')
    max_spaciousness = NumberFilter(field_name='spaciousness', lookup_expr='lte')

    class Meta:
        model = LectureHall
        fields = {
            'code':['exact'],
            'min_spaciousness': ['exact'],
            'max_spaciousness': ['exact'],
            'building': ['exact'],
            'prof_type': ['exact'],
        }


class LectureHallViewSet(viewsets.ModelViewSet):
    '''
    GET: /api/lecture_hall/
    :params
        code: string (номер кабинета)
        min_spaciousness: int
        max_spaciousness: int
        building:
            'V': ул. Павла Корчагина
            'A': ул. Автозаводская
            'E': ул. Большая Семеновская
            'P': ул. Прянишникова
            'S': ул. Садовая-Спасская
        prof_type: (тип дисциплины) допустимые значения 
            'S': 'Простая'
            'C': 'Компьютерная'
            'D': 'Дизайн'
            'L': 'Лаборатория'
            'M': 'Мастерская'

    :code
        200

    :returns
        [
            {
                "id": 1,
                "constraints": {
                    "id": 1,
                    "projector": true,
                    "big_blackboard": true
                },
                "spaciousness": 144,
                "code": "H205",
                "building": "E",
                "prof_type": "S"
            },
            ...
        ]

    GET: /api/lecture_hall/1/
    
    :code
        200

    :returns
        {
            "id": 1,
            "constraints": {
                "id": 1,
                "projector": true,
                "big_blackboard": true
            },
            "spaciousness": 144,
            "code": "H205",
            "building": "E",
            "prof_type": "S"
        }

    POST: /api/lecture_hall/

    :params
        need_projector: bool, required=True
        need_big_blackboard: bool, required=True
        spaciousness: int, required=True
        code: string, required=True
        building: (как в GET), required=True
        prof_type: (как в GET), required=True

    
    :code
        201
    ////////////////////////////////////////
    :returns
        {
            'id': 2, 
            'constraints': {
                'id': 3, 
                'projector': False, 
                'big_blackboard': True
            }, 
            'title': 'Дисциплина2', 
            'prof_type': 'S'
        }


    PUT: /api/lecture_hall/1/
    :params
        need_projector: bool, required=True
        need_big_blackboard: bool, required=True
        spaciousness: int, required=True
        code: string, required=True
        building: (как в GET), required=True
        prof_type: (как в GET), required=True

    :code
        200
    
    :returns
        {
            'id': 2, 
            'constraints': {
                'id': 3, 
                'projector': False, 
                'big_blackboard': True
            }, 
            'title': 'Дисциплина2', 
            'prof_type': 'S'
        }

    DELETE: /api/lecture_hall/1/

    :code
        204
    '''
    queryset = LectureHall.objects.all()  
    serializer_class = LectureHallSerializer 
    filterset_class = LectureHallFilter