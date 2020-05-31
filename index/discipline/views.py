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
        need_blackboard = self.validated_data.pop('need_blackboard')
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
    queryset = Discipline.objects.all()
    filterset_class = DisciplineFilter
