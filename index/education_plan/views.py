from index.education_plan.utils import upload_plan
from index.models import EducationPlan
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import FilterSet, CharFilter
from index.lesson.views import SpecDisciplineSerializer, SpecGroupSerializer


class EducationPlanSerializer(serializers.ModelSerializer):
    discipline = SpecDisciplineSerializer(read_only=True)
    group = SpecGroupSerializer(read_only=True)
    group_id = serializers.IntegerField(write_only=True)
    discipline_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = EducationPlan
        fields = '__all__'

class EducationPlanUploadSerializer(serializers.Serializer):
    TYPE_ALL = 'A'
    TYPE_GROUP = 'G'
    group_id = serializers.IntegerField(required=False, allow_null=True)
    type = serializers.ChoiceField(choices=[TYPE_ALL, TYPE_GROUP])
    file = serializers.FileField()

    def is_valid(self, raise_exception):
        super().is_valid(raise_exception=raise_exception)
        if (self.validated_data['type'] == self.TYPE_GROUP and not self.validated_data.get('group_id')):
            raise serializers.ValidationError('Нужно выбрать группу для типа загрузки через группу.')


class EducationPlanFilter(FilterSet):
    discipline = CharFilter(field_name='discipline', lookup_expr='title__icontains')
    group = CharFilter(field_name='group', lookup_expr='code__icontains')

    class Meta:
        model = EducationPlan
        fields = {
            'discipline':['exact'],
            'group': ['exact'],
        }

        
class EducationPlanViewSet(viewsets.ModelViewSet):
    queryset = EducationPlan.objects.all()
    serializer_class = EducationPlanSerializer
    filterset_class = EducationPlanFilter

    @action(detail=False, methods=['post',])
    def upload(self, request):
        data = EducationPlanUploadSerializer(data=request.data)
        data.is_valid(True)
        upload_plan(data.validated_data['file'].file, data.validated_data)
        return Response()
