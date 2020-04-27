from index.models import EducationPlan
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from index.group.views import GroupSerializer
from index.discipline.views import DisciplineSerializer

class EducationPlanSerializer(serializers.ModelSerializer):
    discipline = DisciplineSerializer()
    group = GroupSerializer()


    class Meta:
        model = EducationPlan
        fields = '__all__'

        
class EducationPlanViewSet(viewsets.ModelViewSet):
    queryset = EducationPlan.objects.all()   
