from rest_framework import serializers
from index.models import Discipline, ConstraintCollection
from index.serializers import ConstraintCollectionSerializer
from rest_framework import viewsets
from django_filters.rest_framework import FilterSet, CharFilter

class DisciplineSerializer(serializers.ModelSerializer):
    constraints = ConstraintCollectionSerializer(read_only=True)
    need_projector = serializers.BooleanField(required=True, write_only=True)
    need_big_blackboard = serializers.BooleanField(required=True, write_only=True)
    class Meta:
        model = Discipline
        fields = '__all__'

    def save(self, *args, **kwargs):
        need_projector = self.validated_data.pop('need_projector')
        need_blackboard = self.validated_data.pop('need_big_blackboard')
        constraints = ConstraintCollection.objects.get(
            projector=need_projector, 
            big_blackboard=need_blackboard
        )
        self.validated_data['constraints'] = constraints
        super(DisciplineSerializer, self).save(*args, **kwargs)


class DisciplineFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Discipline
        fields = {
            'title':['exact'],
            'prof_type': ['exact'],
        }


class DisciplineViewSet(viewsets.ModelViewSet):
    """
    GET: /api/discipline/
    :params
        title: string (название дисциплины)
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
                'id': 1, 
                'constraints': {
                    'id': 3, 
                    'projector': False, 
                    'big_blackboard': True
                }, 
                'title': 'Дисциплина4', 
                'prof_type': 'C'
            },
            ...
        ]

    GET: /api/discipline/1/
    
    :code
        200

    :returns
        {
            'id': 1, 
            'constraints': {
                'id': 3, 
                'projector': False, 
                'big_blackboard': True
            }, 
            'title': 'Дисциплина4', 
            'prof_type': 'C'
        }

    POST: /api/discipline/

    :params
        need_projector: bool, required=True
        need_big_blackboard: bool, required=True
        title: string, required=True
        prof_type: string (как в GET), required=True
    
    :code
        201
    
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


    PUT: /api/discipline/1/
    :params
        need_projector: bool, required=True
        need_big_blackboard: bool, required=True
        title: string, required=True
        prof_type: string (как в GET), required=True

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

    DELETE: /api/discipline/1/

    :code
        204

    """

    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer
    filterset_class = DisciplineFilter
