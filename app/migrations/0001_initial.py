# Generated by Django 5.0 on 2023-12-19 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FaceDetectionJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_time', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'app_face_detection_schedules',
            },
        ),
    ]
