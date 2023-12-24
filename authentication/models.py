from django.db import models
from django.contrib.auth.models import User


class UserBusinessType(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'auth_user_business_type'


class UserBusiness(models.Model):
    name = models.CharField(max_length=128, default='')
    watermark = models.ImageField(upload_to='user/watermarks/', null=True, blank=True)
    business_type = models.ForeignKey(UserBusinessType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'auth_user_business'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business = models.OneToOneField(UserBusiness, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='user/profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'auth_user_profile'


