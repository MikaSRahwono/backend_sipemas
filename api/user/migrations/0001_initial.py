# Generated by Django 5.0.4 on 2024-04-25 16:00

import api.user.storage
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('marketplace', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.CharField(max_length=11, primary_key=True, serialize=False)),
                ('faculty', models.CharField(blank=True, choices=[('ILMU KOMPUTER', 'Ilmu Komputer')], default='ILMU KOMPUTER', max_length=256)),
                ('study_program', models.CharField(blank=True, max_length=256)),
                ('educational_program', models.CharField(blank=True, max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=256)),
                ('role', models.CharField(choices=[('STA', 'Staf'), ('LEC', 'Dosen'), ('STU', 'Mahasiswa')], default='STU', max_length=3)),
                ('is_external', models.BooleanField(default=False)),
                ('organization', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='organization', to='user.organization')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_detail', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('major', models.CharField(max_length=256)),
                ('about', models.TextField(blank=True)),
                ('profile_image', models.ImageField(blank=True, null=True, storage=api.user.storage.ImageStorage(), upload_to='profile_imgs/')),
                ('line_id', models.CharField(blank=True, max_length=256)),
                ('linkedin_url', models.CharField(blank=True, max_length=256)),
                ('github_url', models.CharField(blank=True, max_length=256)),
                ('is_open', models.BooleanField(default=True)),
                ('fields', models.ManyToManyField(related_name='field_of_interest', to='marketplace.field')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userprofile')),
            ],
        ),
    ]
