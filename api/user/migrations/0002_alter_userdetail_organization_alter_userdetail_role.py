# Generated by Django 5.0.4 on 2024-05-29 08:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization', to='user.organization'),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='role',
            field=models.CharField(choices=[('SEC', 'Secretary'), ('LEC', 'Dosen'), ('STU', 'Mahasiswa')], default='STU', max_length=3),
        ),
    ]
