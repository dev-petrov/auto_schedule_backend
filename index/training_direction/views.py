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
    queryset = TrainingDirection.objects.all()   
    filterset_class = TrainingDirectionFilter