from index.models import LectureHall, ConstraintCollection, Lesson
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from index.serializers import ConstraintCollectionSerializer
from django_filters.rest_framework import FilterSet, CharFilter, NumberFilter


class LectureHallSerializer(serializers.ModelSerializer):
    constraints = ConstraintCollectionSerializer(read_only=True)
    has_projector = serializers.BooleanField(write_only=True)
    has_big_blackboard = serializers.BooleanField(write_only=True)

    class Meta:
        model = LectureHall
        fields = '__all__'

    def save(self, *args, **kwargs):
        has_projector = self.validated_data.pop('has_projector')
        has_blackboard = self.validated_data.pop('has_big_blackboard')
        constraints = ConstraintCollection.objects.get(
            projector=has_projector, 
            big_blackboard=has_blackboard
        )
        self.validated_data['constraints'] = constraints
        super(LectureHallSerializer, self).save(*args, **kwargs)


class LectureHallFilter(FilterSet):
    code = CharFilter(field_name='code', lookup_expr='icontains')
    min_spaciousness = NumberFilter(field_name='spaciousness', lookup_expr='gte')
    max_spaciousness = NumberFilter(field_name='spaciousness', lookup_expr='lte')

    class Meta:
        model = LectureHall
        fields = {
            'code':['exact'],
            'min_spaciousness': ['exact'],
            'max_spaciousness': ['exact'],
            'building': ['exact'],
            'prof_type': ['exact'],
        }


class LectureHallViewSet(viewsets.ModelViewSet):
    queryset = LectureHall.objects.all()  
    serializer_class = LectureHallSerializer 
    filterset_class = LectureHallFilter

    @action(detail=False, methods=['get'],)
    def efficiency(self, request):
        code = request.query_params.get('code')
        building = request.query_params.get('building')
        lecture_halls = LectureHall.objects.all()
        if code:
            lecture_halls = lecture_halls.filter(code__icontains=code)

        if building:
            lecture_halls = lecture_halls.filter(building=building)
        lecture_halls = list(lecture_halls)
        default_eff = {
            1: [True, True, True, True, True, True, True,],
            2: [True, True, True, True, True, True, True,],
            3: [True, True, True, True, True, True, True,],
            4: [True, True, True, True, True, True, True,],
            5: [True, True, True, True, True, True, True,],
            6: [True, True, True, True, True, True, True,],
        }
        response = {
            lh.id: default_eff
            for lh in lecture_halls
        }

        for lesson in Lesson.objects.filter(lecture_hall__in=lecture_halls):
            response[lesson.lecture_hall_id][lesson.day_of_week][lesson.lesson - 1] = False
        
        return Response(response)

