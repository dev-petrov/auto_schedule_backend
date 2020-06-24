# Generated by Django 3.0.3 on 2020-06-24 11:37

from django.db import migrations, models
import django.db.models.deletion

def create_constraints(apps, schema_editor):
    ConstraintCollection = apps.get_model('index', 'ConstraintCollection')
    constraints = [
        ConstraintCollection(
            projector=v1,
            big_blackboard=v2,
        )
        for v1 in [True, False]
        for v2 in [True, False]
    ]
    ConstraintCollection.objects.bulk_create(constraints)

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConstraintCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projector', models.BooleanField(default=False)),
                ('big_blackboard', models.BooleanField(default=False)),
            ],
            options={
                'unique_together': {('projector', 'big_blackboard')},
            },
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('prof_type', models.CharField(choices=[('S', 'Обычная'), ('C', 'Компьютерная'), ('D', 'Дизайн'), ('L', 'Лаборатория'), ('M', 'Мастерская')], default='S', max_length=1)),
                ('type', models.CharField(choices=[('L', 'Лекция'), ('P', 'Практика'), ('LB', 'Лаб. работа')], default='L', max_length=2)),
                ('constraints', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='index.ConstraintCollection')),
            ],
        ),
        migrations.CreateModel(
            name='EducationPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.IntegerField()),
                ('constraints', models.TextField(null=True)),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='index.Discipline')),
            ],
        ),
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='LectureHall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spaciousness', models.IntegerField()),
                ('code', models.CharField(max_length=10)),
                ('building', models.CharField(choices=[('V', 'ул. Павла Корчагина'), ('A', 'ул. Автозаводская'), ('E', 'ул. Большая Семеновская'), ('P', 'ул. Прянишникова'), ('S', 'ул. Садовая-Спасская')], default='E', max_length=1)),
                ('prof_type', models.CharField(choices=[('S', 'Обычная'), ('C', 'Компьютерная'), ('D', 'Дизайн'), ('L', 'Лаборатория'), ('M', 'Мастерская')], default='S', max_length=1)),
                ('constraints', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='index.ConstraintCollection')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('constraints', models.TextField(default='{"buildings_priority": ["E", "A", "V", "S", "P"], "day_constraints": {"1": [true, true, true, true, true, true, true], "2": [true, true, true, true, true, true, true], "3": [true, true, true, true, true, true, true], "4": [true, true, true, true, true, true, true], "5": [true, true, true, true, true, true, true], "6": [true, true, true, true, true, true, true]}}')),
                ('total_hours', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TrainingDirection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('B', 'Бакалавриат'), ('S', 'Специалитет'), ('M', 'Магистратура')], default='B', max_length=1)),
                ('constraints', models.TextField(default='{"buildings": ["E", "A", "P", "V", "S"], "day_constraints": {"1": [true, true, true, true, true, true, true], "2": [true, true, true, true, true, true, true], "3": [true, true, true, true, true, true, true], "4": [true, true, true, true, true, true, true], "5": [true, true, true, true, true, true, true], "6": [true, true, true, true, true, true, true]}}', verbose_name='Ограничения направления')),
            ],
        ),
        migrations.CreateModel(
            name='TeacherDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='index.Discipline')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='details', to='index.Teacher')),
            ],
            options={
                'unique_together': {('discipline', 'teacher')},
            },
        ),
        migrations.AddField(
            model_name='teacher',
            name='disciplines',
            field=models.ManyToManyField(related_name='teachers', through='index.TeacherDetails', to='index.Discipline'),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=7)),
                ('count_of_students', models.IntegerField()),
                ('disciplines', models.ManyToManyField(related_name='groups', through='index.EducationPlan', to='index.Discipline')),
                ('flow', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='index.Flow')),
                ('training_direction', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='index.TrainingDirection')),
            ],
        ),
        migrations.AddField(
            model_name='educationplan',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='index.Group'),
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson', models.IntegerField(choices=[(1, 'Первая пара'), (2, 'Вторая пара'), (3, 'Третья пара'), (4, 'Четвёртая пара'), (5, 'Пятая пара'), (6, 'Шестая пара'), (7, 'Седьмая пара')], default=1)),
                ('day_of_week', models.IntegerField(choices=[(1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда'), (4, 'Четверг'), (5, 'Пятница'), (6, 'Суббота')], default=1)),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='index.Discipline')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='index.Group')),
                ('lecture_hall', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='index.LectureHall')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='index.Teacher')),
            ],
            options={
                'unique_together': {('group', 'lesson', 'day_of_week'), ('teacher', 'lesson', 'day_of_week')},
            },
        ),
        migrations.RunPython(create_constraints),
    ]
