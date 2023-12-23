from django.db import models
from django.contrib.auth.models import User


class UserDesignation(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'auth_user_designations'


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='user/profile_pics/', null=True, blank=True)
    designation = models.ForeignKey(UserDesignation, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'auth_user_profile'
