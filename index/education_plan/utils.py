import pandas as pd
from rest_framework import serializers
from index.models import Discipline, EducationPlan, Group

def upload_plan(file, data):
    try:
        df = pd.read_excel(file if isinstance(file, str) else file.read(), engine='openpyxl')
    except:
        raise serializers.ValidationError('Неправильный формат файла')
    type = data['type']
    disciplines = {
        d.title: d
        for d in Discipline.objects.all()
    }
    plans = []
    if type == 'A':
        COL_GROUP = df.columns[0]
        COL_DISCIPLINE = df.columns[1]
        COL_COUNT = df.columns[2]
        groups = {
            g.code: g
            for g in Group.objects.all()
        }
        for i, row in df.iterrows():
            group = groups.get(row[COL_GROUP])
            discipline = disciplines.get(row[COL_DISCIPLINE])
            if not group:
                raise serializers.ValidationError(f'Группы с кодом {row[COL_GROUP]} на строчке {i + 2} не сущестует')
            if not discipline:
                raise serializers.ValidationError(f'Дисциплины {row[COL_DISCIPLINE]} на строчке {i + 2} не сущестует')
            plans.append(EducationPlan(
                group=group,
                discipline=discipline,
                lessons_in_week=row[COL_COUNT],
            ))
        EducationPlan.objects.filter(group__code__in=df[COL_GROUP].unique()).delete()
    else:
        COL_DISCIPLINE = df.columns[0]
        COL_COUNT = df.columns[1]
        group_id = data['group_id']
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

    return True
