from index.models import LectureHall
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from index.serializers import ConstraintCollectionSerializer

class LectureHallSerializer(serializers.ModelSerializer):
    constraints = ConstraintCollectionSerializer()

    class Meta:
        model = LectureHall
        fields = '__all__'

        
class LectureHallViewSet(viewsets.ModelViewSet):
    queryset = LectureHall.objects.all()   
