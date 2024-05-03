# Generated by Django 5.0.4 on 2024-05-03 17:22

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('kd_mk', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('nm_mk', models.CharField(max_length=256)),
                ('sks', models.IntegerField()),
                ('course_type', models.CharField(choices=[('OO', 'One to One'), ('OM', 'One to Many')], max_length=2)),
                ('is_allowed_new_topic', models.BooleanField()),
                ('topic_count', models.IntegerField(default=0)),
                ('allowed_organizations', models.ManyToManyField(related_name='prodi', to='user.organization')),
            ],
            options={
                'verbose_name_plural': 'courses',
            },
        ),
        migrations.CreateModel(
            name='ActivityStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('name', models.CharField(max_length=256)),
                ('type', models.CharField(choices=[('INF', 'Step Information'), ('ASG', 'Step Assignment'), ('SID', 'Step Sidang')], default='INF', max_length=3)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.course')),
            ],
            options={
                'unique_together': {('course', 'index')},
            },
        ),
        migrations.CreateModel(
            name='CourseInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('html', ckeditor.fields.RichTextField()),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='academic.course')),
            ],
        ),
        migrations.CreateModel(
            name='Prerequisite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('SKS', 'Jumlah SKS'), ('SMT', 'Semester'), ('CRS', 'Mata Kuliah')], default='SKS', max_length=3)),
                ('minimum', models.IntegerField(default=0)),
                ('maximum', models.IntegerField(blank=True, default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.course')),
            ],
        ),
        migrations.CreateModel(
            name='StepAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=256, null=True)),
                ('subheading', models.CharField(max_length=256, null=True)),
                ('activity_step', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='academic.activitystep')),
            ],
        ),
        migrations.CreateModel(
            name='StepComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('type', models.CharField(choices=[('INF', 'Information Component'), ('ASG', 'Assignment Component'), ('ANN', 'Announcement Component')], default='INF', max_length=3)),
                ('activity_step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stepcomponents', to='academic.activitystep')),
            ],
            options={
                'unique_together': {('activity_step', 'index')},
            },
        ),
        migrations.CreateModel(
            name='InformationComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=256)),
                ('subheading', models.CharField(max_length=256)),
                ('paragraph', models.TextField()),
                ('step_component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='informationcomponents', to='academic.stepcomponent')),
            ],
        ),
        migrations.CreateModel(
            name='AssignmentComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('subtitle', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('LOG', 'Log Assignment'), ('SUB', 'Submission Assignent')], default='SUB', max_length=3)),
                ('step_component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='assignmentcomponents', to='academic.stepcomponent')),
            ],
        ),
        migrations.CreateModel(
            name='AnnouncementComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=256)),
                ('subheading', models.CharField(max_length=256)),
                ('paragraph', models.TextField()),
                ('step_component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcementcomponents', to='academic.stepcomponent')),
            ],
        ),
        migrations.CreateModel(
            name='StepInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=256, null=True)),
                ('subheading', models.CharField(max_length=256, null=True)),
                ('html', ckeditor.fields.RichTextField()),
                ('activity_step', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='academic.activitystep')),
            ],
        ),
        migrations.CreateModel(
            name='StepSidang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=256)),
                ('subheading', models.CharField(max_length=256)),
                ('paragraph', models.TextField()),
                ('activity_step', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='academic.activitystep')),
            ],
        ),
    ]
