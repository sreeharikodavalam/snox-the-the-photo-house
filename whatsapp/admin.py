from django.contrib import admin
from .models import WhatsappLogSharedPhoto, WhatsappLogWelcomeMessage, WhatsappSender


admin.site.register(WhatsappLogSharedPhoto)
admin.site.register(WhatsappLogWelcomeMessage)
admin.site.register(WhatsappSender)
