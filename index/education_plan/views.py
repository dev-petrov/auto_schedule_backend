import pandas as pd
from index.models import Discipline, EducationPlan, Group
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
        try:
            df = pd.read_excel(data.validated_data['file'].file.read(), engine='openpyxl')
        except:
            raise serializers.ValidationError('Неправильный формат файла')
        type = data.validated_data['type']
        disciplines = {
            d.title: d
            for d in Discipline.objects.all()
        }
        plans = []
        if type == EducationPlanUploadSerializer.TYPE_ALL:
            COL_GROUP = df.columns[0]
            COL_DISCIPLINE = df.columns[1]
            COL_COUNT = df.columns[2]
            groups = {
                g.code: g
                for g in Group.objects.all()
            }
            for _, row in df.iterrows():
                group = groups.get(row[COL_GROUP])
                discipline = disciplines.get(row[COL_DISCIPLINE])
                if not group:
                    raise serializers.ValidationError(f'Группы с кодом {row[COL_GROUP]} не сущестует')
                if not discipline:
                    raise serializers.ValidationError(f'Дисциплины {row[COL_DISCIPLINE]} не сущестует')
                plans.append(EducationPlan(
                    group=group,
                    discipline=discipline,
                    lessons_in_week=row[COL_COUNT],
                ))
            EducationPlan.objects.filter(group__code__in=df[COL_GROUP].unique()).delete()
        else:
            COL_DISCIPLINE = df.columns[0]
            COL_COUNT = df.columns[1]
            group_id = data.validated_data['group_id']
            for _, row in df.iterrows():
                discipline = disciplines.get(row[COL_DISCIPLINE])
                if not discipline:
                    raise serializers.ValidationError(f'Дисциплины {row[COL_DISCIPLINE]} не сущестует')
                plans.append(EducationPlan(
                    group_id=group_id,
                    discipline=discipline,
                    lessons_in_week=row[COL_COUNT],
                ))
            EducationPlan.objects.filter(group_id=group_id).delete()
        
        EducationPlan.objects.bulk_create(plans)

        return Response()
