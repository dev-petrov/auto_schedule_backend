from index.models import TrainingDirection
from rest_framework import serializers, viewsets
from rest_framework.response import Response

class TrainingDirectionSerializer(serializers.ModelSerializer):
    constraints = serializers.JSONField()

    class Meta:
        model = TrainingDirection
        fields = '__all__'

        
class TrainingDirectionViewSet(viewsets.ModelViewSet):
    queryset = TrainingDirection.objects.all()   
