from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from snoxpro import settings
from events.views import selfie_register

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('events/', include('events.urls')),
    path('register/<int:event_id>/', selfie_register, name='selfie_register'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
