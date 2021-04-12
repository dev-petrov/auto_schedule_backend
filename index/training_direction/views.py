from index.models import TrainingDirection, LessonTrainingDirectionConstraint, BuildingTrainingDirectionConstraint
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from django_filters.rest_framework import FilterSet, CharFilter
from rest_framework.decorators import action


class LessonTrainingDirectionConstraintSerializer(serializers.ModelSerializer):
    training_direction_id = serializers.IntegerField(required=False)
    class Meta:
        model = LessonTrainingDirectionConstraint
        fields = ['id', 'lesson', 'day_of_week', 'training_direction_id']


class BuildingTrainingDirectionConstraintSerializer(serializers.ModelSerializer):
    training_direction_id = serializers.IntegerField(required=False)
    class Meta:
        model = BuildingTrainingDirectionConstraint
        fields = ['id', 'building_id', 'training_direction_id', 'ordering']


class TrainingDirectionSerializer(serializers.ModelSerializer):
    constraints = LessonTrainingDirectionConstraintSerializer(many=True, read_only=True)
    building_constraints = BuildingTrainingDirectionConstraintSerializer(many=True, read_only=True)

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
    serializer_class = TrainingDirectionSerializer 
    filterset_class = TrainingDirectionFilter

    @action(detail=True, methods=['post'])
    def set_lesson_constraints(self, request, pk=None):
        constraints = LessonTrainingDirectionConstraintSerializer(data=request.data, many=True)
        constraints.is_valid(raise_exception=True)

        ids_to_delete = []
        constraints_to_create = []
        for constraint in constraints:
            if constraint.get('id'):
                if constraint.get('delete'):
                    ids_to_delete.append(constraint['id'])
                continue
            constraints_to_create.append(
                LessonTrainingDirectionConstraint(
                    lesson=constraint['lesson'],
                    day_of_week=constraint['day_of_week'],
                    training_direction_id=pk,
                )
            )
        LessonTrainingDirectionConstraint.objects.filter(id__in=ids_to_delete).delete()
        LessonTrainingDirectionConstraint.objects.bulk_create(constraints_to_create)

        return Response()

    @action(detail=True, methods=['post'])
    def set_building_constraints(self, request, pk=None):
        constraints = BuildingTrainingDirectionConstraintSerializer(data=request.data, many=True)
        constraints.is_valid(raise_exception=True)

        ids_to_delete = []
        constraints_to_create = []
        for constraint in constraints:
            if constraint.get('id'):
                if constraint.get('delete'):
                    ids_to_delete.append(constraint['id'])
                continue
            constraints_to_create.append(
                BuildingTrainingDirectionConstraint(
                    lesson=constraint['lesson'],
                    day_of_week=constraint['day_of_week'],
                    training_direction_id=pk,
                )
            )
        BuildingTrainingDirectionConstraint.objects.filter(id__in=ids_to_delete).delete()
        BuildingTrainingDirectionConstraint.objects.bulk_create(constraints_to_create)

        return Response()
    