from django.contrib import admin
from .models import WhatsappLogSharedPhotos, WhatsappLogWelcomeMessages


admin.site.register(WhatsappLogSharedPhotos)
admin.site.register(WhatsappLogWelcomeMessages)
