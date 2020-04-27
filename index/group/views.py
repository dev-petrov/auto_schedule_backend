from index.models import Group
from index.serializers import FlowSerializer
from rest_framework import serializers, viewsets
from rest_framework.response import Response

class GroupSerializer(serializers.ModelSerializer):
    constraints = serializers.JSONField()
    flow = FlowSerialzer()

    class Meta:
        model = Group
        fields = '__all__'

        
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()   
