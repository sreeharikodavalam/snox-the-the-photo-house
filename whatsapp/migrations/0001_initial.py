# Generated by Django 4.2.8 on 2023-12-18 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0007_userselfieregistration_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhatsappLogWelcomeMessages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.CharField(max_length=34)),
                ('send_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='WhatsappLogSharedPhotos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.CharField(max_length=34)),
                ('send_time', models.DateTimeField()),
                ('gallery_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.galleryimage')),
            ],
        ),
    ]