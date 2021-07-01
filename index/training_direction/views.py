from index.models import TrainingDirection, LessonTrainingDirectionConstraint, BuildingTrainingDirectionConstraint
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from django_filters.rest_framework import FilterSet, CharFilter
from rest_framework.decorators import action


class LessonTrainingDirectionConstraintSerializer(serializers.Serializer):
    training_direction_id = serializers.IntegerField(required=False)
    id = serializers.IntegerField(required=False)
    lesson = serializers.IntegerField()
    day_of_week = serializers.IntegerField()
    remove = serializers.BooleanField(default=False)


class BuildingTrainingDirectionConstraintSerializer(serializers.Serializer):
    training_direction_id = serializers.IntegerField(required=False)
    id = serializers.IntegerField(required=False)
    building_id = serializers.IntegerField()
    ordering = serializers.IntegerField()
    remove = serializers.BooleanField(default=False)


class TrainingDirectionSerializer(serializers.ModelSerializer):
    constraints = LessonTrainingDirectionConstraintSerializer(many=True)
    building_constraints = BuildingTrainingDirectionConstraintSerializer(many=True)

    class Meta:
        model = TrainingDirection
        fields = '__all__'

    def _set_lesson_constraints(self, constraints, pk):
        ids_to_delete = []
        constraints_to_create = []
        for constraint in constraints:
            if constraint.get('id'):
                if constraint.get('remove'):
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
        return True

    def _set_building_constraints(self, constraints, pk):
        ids_to_delete = []
        update_ordering = {}
        constraints_to_create = []
        for constraint in constraints:
            if constraint.get('id'):
                if constraint.get('remove'):
                    ids_to_delete.append(constraint['id'])
                else:
                    update_ordering[constraint['id']] = constraint['ordering']
                continue
            constraints_to_create.append(
                BuildingTrainingDirectionConstraint(
                    building_id=constraint['building_id'],
                    ordering=constraint['ordering'],
                    training_direction_id=pk,
                )
            )
        BuildingTrainingDirectionConstraint.objects.filter(id__in=ids_to_delete).delete()
        BuildingTrainingDirectionConstraint.objects.bulk_create(constraints_to_create)
        buildings_to_update = list(BuildingTrainingDirectionConstraint.objects.filter(id__in=update_ordering.keys()))
        for building in buildings_to_update:
            building.ordering = update_ordering[building.id]
        BuildingTrainingDirectionConstraint.objects.bulk_update(buildings_to_update, ['ordering',])


    def create(self, validated_data):
        constraints = validated_data.pop('constraints', [])
        building_constraints = validated_data.pop('building_constraints', [])
        training_direction = super().create(validated_data)
        self._set_lesson_constraints(constraints, training_direction.id)
        self._set_building_constraints(building_constraints, training_direction.id)
        return training_direction

    def update(self, instance, validated_data):
        constraints = validated_data.pop('constraints', [])
        building_constraints = validated_data.pop('building_constraints', [])
        training_direction = super().update(instance, validated_data)
        self._set_lesson_constraints(constraints, training_direction.id)
        self._set_building_constraints(building_constraints, training_direction.id)
        return training_direction


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
