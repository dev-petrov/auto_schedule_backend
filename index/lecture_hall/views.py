from index.models import LectureHall
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from index.serializers import ConstraintCollectionSerializer

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

        
class LectureHallViewSet(viewsets.ModelViewSet):
    queryset = LectureHall.objects.all()   
