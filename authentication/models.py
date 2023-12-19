from django.db import models
from django.contrib.auth.models import User


class UserDesignation(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'auth_user_designations'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='user/profile_pics/', null=True, blank=True)
    designation = models.OneToOneField(UserDesignation, on_delete=models.CASCADE)

    class Meta:
        db_table = 'auth_user_profile'
