from django.contrib import admin
from .models import *

admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(Gallery)
admin.site.register(GalleryImage)
admin.site.register(CroppedGalleryFace)
admin.site.register(UserSelfieRegistration)
