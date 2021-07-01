from index.models import Group
from rest_framework import serializers, viewsets
from index.flow.views import FlowSerializer
from django_filters.rest_framework import FilterSet, CharFilter, NumberFilter
from index.training_direction.views import TrainingDirectionSerializer
from index.lesson.views import SpecDisciplineSerializer


class GroupSerializer(serializers.ModelSerializer):
    constraints = serializers.JSONField(required=False)
    flow = FlowSerializer(read_only=True)
    flow_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    training_direction = TrainingDirectionSerializer(read_only=True)
    training_direction_id = serializers.IntegerField(write_only=True)
    disciplines = SpecDisciplineSerializer(many=True, read_only=True)

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
    queryset = Group.objects.prefetch_related('training_direction__constraints').all()  
    serializer_class = GroupSerializer
    filterset_class = GroupFilter 
