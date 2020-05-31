from index.models import Teacher, Discipline, TeacherDetails
from index.discipline.views import DisciplineSerializer
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from django_filters.rest_framework import FilterSet, CharFilter


class TeacherSerializer(serializers.ModelSerializer):
    disciplines = DisciplineSerializer(many=True, read_only=True)
    constraints = serializers.JSONField()
    disciplines_ids = serializers.ListField(write_only=True)

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'middle_name', 'disciplines', 'constraints', 'total_hours', 'disciplines_ids']


class TeacherFilter(FilterSet):
    first_name = CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = CharFilter(field_name='last_name', lookup_expr='icontains')
    middle_name = CharFilter(field_name='middle_name', lookup_expr='icontains')
    
    class Meta:
        model = Teacher
        fields = {
            'first_name':['exact'],
            'last_name': ['exact'],
            'middle_name': ['exact'],
            'disciplines': ['exact', 'in'],
        }

        
class TeacherViewSet(viewsets.ModelViewSet):
    '''
    GET: /api/teacher/

    :params
        first_name: string
        last_name: string
        middle_name: string
        disciplines: int / list(int) #discipline_id

    :code
        200

    :returns
        [
            {
                "first_name": "Васильев",
                "last_name": "Васильев",
                "middle_name": "Борисович",
                "disciplines": [
                    {
                        "id": 9,
                        "constraints": {
                            "id": 1,
                            "projector": true,
                            "big_blackboard": true
                        },
                        "title": "Физика",
                        "prof_type": "S"
                    },
                    {
                        "id": 8,
                        "constraints": {
                            "id": 3,
                            "projector": false,
                            "big_blackboard": true
                        },
                        "title": "Веб-разработка",
                        "prof_type": "C"
                    }
                ],
                "constraints": "{\"buildings_priority\": [\"E\", \"A\", \"P\", \"S\", \"V\"], \"day_constraints\": {\"MO\": [true, false, true, true, true, false, true], \"TU\": [true, true, true, false, true, false, false], \"WE\": [true, false, false, true, true, true, true], \"TH\": [true, false, true, true, false, true, false], \"FR\": [true, true, false, true, true, true, true], \"SA\": [true, false, true, true, true, false, true]}}",
                "total_hours": 12
            },
            ...
        ]
    
    GET /api/teacher/1/

    :code
        200

    :returns
        {
            "first_name": "Васильев",
            "last_name": "Васильев",
            "middle_name": "Борисович",
            "disciplines": [
                {
                    "id": 9,
                    "constraints": {
                        "id": 1,
                        "projector": true,
                        "big_blackboard": true
                    },
                    "title": "Физика",
                    "prof_type": "S"
                },
                {
                    "id": 8,
                    "constraints": {
                        "id": 3,
                        "projector": false,
                        "big_blackboard": true
                    },
                    "title": "Веб-разработка",
                    "prof_type": "C"
                }
            ],
            "constraints": "{\"buildings_priority\": [\"E\", \"A\", \"P\", \"S\", \"V\"], \"day_constraints\": {\"MO\": [true, false, true, true, true, false, true], \"TU\": [true, true, true, false, true, false, false], \"WE\": [true, false, false, true, true, true, true], \"TH\": [true, false, true, true, false, true, false], \"FR\": [true, true, false, true, true, true, true], \"SA\": [true, false, true, true, true, false, true]}}",
            "total_hours": 12
        }

    POST: /api/teacher/

    :params
        first_name: string, required=True
        last_name: string, required=True
        middle_name: string, required=True
        constraints: JSON field, required=True
        total_hours: int, required=True
        disciplines_ids: list(int)?, required=True
    
    :code
        201
    
    :returns
        {
            "first_name": "aa",
            "last_name": "aa",
            "middle_name": "aa",
            "disciplines": [
                {
                    "id": 1,
                    "constraints": {
                        "id": 3,
                        "projector": false,
                        "big_blackboard": true
                    },
                    "title": "Линейная алгебра",
                    "prof_type": "S"
                }
            ],
            "constraints": {
                "buildings_priority": [
                    "E",
                    "A",
                    "P",
                    "S",
                    "V"
                ],
                "day_constraints": {
                    "MO": [
                        true,
                        false,
                        true,
                        true,
                        true,
                        false,
                        true
                    ],
                    "TU": [
                        true,
                        true,
                        true,
                        false,
                        true,
                        false,
                        false
                    ],
                    "WE": [
                        true,
                        false,
                        false,
                        true,
                        true,
                        true,
                        true
                    ],
                    "TH": [
                        true,
                        false,
                        true,
                        true,
                        false,
                        true,
                        false
                    ],
                    "FR": [
                        true,
                        true,
                        false,
                        true,
                        true,
                        true,
                        true
                    ],
                    "SA": [
                        true,
                        false,
                        true,
                        true,
                        true,
                        false,
                        true
                    ]
                }
            },
            "total_hours": 5
        }


    PUT: /api/teacher/1/

    :params
        first_name: string, required=True
        last_name: string, required=True
        middle_name: string, required=True
        constraints: JSON field, required=True
        total_hours: int, required=True
        disciplines: JSON?, required=True

    :code
        200
    
    :returns
        {
            "first_name": "Васильев",
            "last_name": "Васильев",
            "middle_name": "Борисович",
            "disciplines": [
                {
                    "id": 1,
                    "constraints": {
                        "id": 3,
                        "projector": false,
                        "big_blackboard": true
                    },
                    "title": "Линейная алгебра",
                    "prof_type": "S"
                }
            ],
            "constraints": "{\"buildings_priority\": [\"E\", \"A\", \"P\", \"S\", \"V\"], \"day_constraints\": {\"MO\": [true, false, true, true, true, false, true], \"TU\": [true, true, true, false, true, false, false], \"WE\": [true, false, false, true, true, true, true], \"TH\": [true, false, true, true, false, true, false], \"FR\": [true, true, false, true, true, true, true], \"SA\": [true, false, true, true, true, false, true]}}",
            "total_hours": 12
        }

    DELETE: /api/teacher/1/

    :code
        204

    '''
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
    filterset_class = TeacherFilter

    def create(self, request):
        data = TeacherSerializer(data=request.data)

        data.is_valid(raise_exception=True)

        disciplines_ids = data.validated_data.pop('disciplines_ids', [])

        data.save()

        teacher = data.instance

        details = [
            TeacherDetails(teacher=teacher,
            discipline_id=discipline_id)
            for discipline_id in disciplines_ids
        ]

        TeacherDetails.objects.bulk_create(details)

        return Response(TeacherSerializer(instance=teacher).data)

    
    def update(self, request, pk=None):
        teacher = Teacher.objects.get(pk=pk)

        data = TeacherSerializer(data=request.data, instance=teacher)

        data.is_valid(raise_exception=True)

        disciplines_ids = data.validated_data.pop('disciplines_ids', [])

        data.save()

        teacher.details.all().delete()

        details = [
            TeacherDetails(teacher=teacher,
            discipline_id=discipline_id)
            for discipline_id in disciplines_ids
        ]

        TeacherDetails.objects.bulk_create(details)

        return Response(TeacherSerializer(instance=teacher).data)
