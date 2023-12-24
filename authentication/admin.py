from django.contrib import admin
from .models import UserProfile, UserBusinessType, UserBusiness

admin.site.register(UserProfile)
admin.site.register(UserBusinessType)
admin.site.register(UserBusiness)
