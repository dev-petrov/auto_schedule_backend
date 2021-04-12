from rest_framework import serializers
from index.models import Building
from rest_framework import viewsets
from django_filters.rest_framework import FilterSet, CharFilter

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'


class BuildingFilter(FilterSet):
    code = CharFilter(field_name='code', lookup_expr='icontains')


class BuildingViewSet(viewsets.ModelViewSet):

    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    filterset_class = BuildingFilter
