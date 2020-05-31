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
    queryset = LectureHall.objects.all()   
    filterset_class = LectureHallFilter