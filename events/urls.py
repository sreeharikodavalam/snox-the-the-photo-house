from django.urls import path
from .views import *

urlpatterns = [
    path('', list_events, name='list_events'),
    path('create/', create_event, name='create_event'),
    path('edit/<int:event_id>/', edit_event, name='edit_event'),
    path('gallery/<int:event_id>/', list_galleries, name='list_gallery'),
    # Image gallery
    path('gallery/create/<int:event_id>/', create_gallery, name='create_gallery'),
    path('gallery/images/upload_process/<int:gallery_id>/', upload_gallery_image_process, name='upload_gallery_image_process'),
    path('gallery/images/upload/<int:gallery_id>/', upload_gallery_image, name='upload_gallery_image'),
    path('gallery/images/<int:gallery_id>/', list_gallery_images, name='list_gallery_images'),
    path('faces/list/<int:event_id>/', face_registration_list, name='list_face_registrations')
]
