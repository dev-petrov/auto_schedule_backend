from rest_framework import serializers
from index.models import Flow
from rest_framework import viewsets
from django_filters.rest_framework import FilterSet, CharFilter

class FlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = '__all__'

    

class FlowFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Flow
        fields = {
            'name':['exact'],
        }


class FlowViewSet(viewsets.ModelViewSet):

    queryset = Flow.objects.all()
    serializer_class = FlowSerializer
    filterset_class = FlowFilter
