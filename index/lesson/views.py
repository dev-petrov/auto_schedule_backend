from algo.algov2 import AlgoV2
from index.models import Lesson, Teacher, Group, EducationPlan, LectureHall, Discipline, TeacherDetails
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, F
from django_filters.rest_framework import FilterSet, CharFilter


TYPES_MESSAGES = {
    Discipline.TYPE_LAB: 'лабораторную',
    Discipline.TYPE_LECTION: 'лекцию',
    Discipline.TYPE_PRACTICE: 'практику',
}


class SpecTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'middle_name']


class SpecGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'code']


class SpecDisciplineSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    prof_type = serializers.CharField()
    type = serializers.CharField()
    short_name = serializers.CharField()


class SpecLectureHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureHall
        fields = ['id', 'code', 'building_id', 'prof_type']


class LessonSerializer(serializers.ModelSerializer):
    discipline = SpecDisciplineSerializer(read_only=True)
    group = SpecGroupSerializer(read_only=True)
    teacher = SpecTeacherSerializer(read_only=True)
    lecture_hall = SpecLectureHallSerializer(read_only=True)
    discipline_id = serializers.IntegerField(write_only=True)
    group_id = serializers.IntegerField(write_only=True)
    teacher_id = serializers.IntegerField(write_only=True)
    lecture_hall_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'
    
    def validate(self, attrs):
        lessons = Lesson.objects.all()
        if self.instance:
            lessons = lessons.exclude(id=self.instance.id)

        teacher_lesson = lessons.filter(
            teacher_id=attrs['teacher_id'],
            lesson=attrs['lesson'],
            day_of_week=attrs['day_of_week'],
        )
        group_lesson = lessons.filter(
            group_id=attrs['group_id'],
            lesson=attrs['lesson'],
            day_of_week=attrs['day_of_week'],
        )
        lecture_hall_lesson = lessons.filter(
            lecture_hall_id=attrs['lecture_hall_id'],
            lesson=attrs['lesson'],
            day_of_week=attrs['day_of_week'],
        )
        discipline = Discipline.objects.get(id=attrs['discipline_id'])
        
        if not TeacherDetails.objects.filter(teacher_id=attrs['teacher_id'], discipline=discipline).exists():
            teacher = Teacher.objects.get(id=attrs['teacher_id'])
            type = TYPES_MESSAGES[discipline.type]
            raise serializers.ValidationError(f'Преподаватель {teacher.last_name} {teacher.first_name} не может вести {type} по предмету {discipline.title}.')


        if not EducationPlan.objects.filter(discipline=discipline, group_id=attrs['group_id'], is_active=True).exists():
            group = Group.objects.get(id=attrs['group_id'])
            raise serializers.ValidationError(f'У группы {group.code} нет дисциплины {discipline.title} в образовательном плане.')

        if discipline.type == Discipline.TYPE_LECTION:
            teacher_lesson = teacher_lesson.exclude(discipline=discipline)
            lecture_hall_lesson = lecture_hall_lesson.exclude(discipline=discipline)
        
        if teacher_lesson.exists():
            raise serializers.ValidationError('У данного преподавателя уже есть пара в это время.')

        if group_lesson.exists():
            raise serializers.ValidationError('У данной группы уже есть пара в это время.')

        if lecture_hall_lesson.exists():
            raise serializers.ValidationError('Данная аудитория занята в это время.')
       
        return attrs


class LessonFilter(FilterSet):
    discipline = CharFilter(field_name='discipline', lookup_expr='discipline__title__icontains')
    group = CharFilter(field_name='group', lookup_expr='code__icontains')
    teacher = CharFilter(field_name='teacher', method='filter_teacher')
    lecture_hall = CharFilter(field_name='lecture_hall', lookup_expr='code__icontains')


    def filter_teacher(self, queryset, name, value):
        values = value.split(',')
        q = Q()
        for val in values:
            q |= Q(teacher__first_name__icontains=val)
            q |= Q(teacher__last_name__icontains=val)
            q |= Q(teacher__middle_name__icontains=val)
        return queryset.filter(q)

    class Meta:
        model = Lesson
        fields = {
            'discipline':['exact'],
            'group': ['exact'],
            'teacher': ['exact', 'in'],
            'lecture_hall': ['exact'],
        }

        
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()   
    serializer_class = LessonSerializer
    filterset_class = LessonFilter

    @action(detail=False, methods=['post',])
    def create_schedule(self, request):
        algo = AlgoV2()
        schedule = algo.create_schedule()
        Lesson.objects.all().delete()
        Lesson.objects.bulk_create(
            Lesson(**row)
            for i, row in schedule.iterrows()
        )
        return Response()
    