# Generated by Django 5.0 on 2023-12-19 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_userprofile_designation'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='userdesignation',
            table='user_designations',
        ),
        migrations.AlterModelTable(
            name='userprofile',
            table='user_profile',
        ),
    ]
