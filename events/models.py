from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class EventType(models.Model):
    event_type_name = models.CharField(max_length=64)
    separation = models.CharField(max_length=6)
    names_count = models.SmallIntegerField()

    class Meta:
        db_table = 'event_type'

    def __str__(self):
        return self.event_type_name


# class EventNames(models.Model):
#     event = models.OneToOneField(Event, on_delete=models.CASCADE)
#     name = models.CharField(max_length=64)


class Event(models.Model):
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, default=1, null=True)
    bride_name = models.CharField(max_length=64, default='')
    groom_name = models.CharField(max_length=64, default='')
    date = models.DateField(default=None)
    venue = models.CharField(max_length=64, default='')
    note = models.CharField(max_length=512, default='')
    cover_image = models.ImageField(upload_to='events/cover', default='')
    created_at = models.DateTimeField(default=timezone.now, editable=True)
    updated_at = models.DateTimeField(default=timezone.now, editable=True)

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()
        else:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def title(self):
        return f"{self.groom_name} {self.event_type.separation} {self.bride_name}"

    def __str__(self):
        return self.title()

    class Meta:
        db_table = 'event_master'


class Gallery(models.Model):
    name = models.CharField(max_length=32)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'event_gallery'


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    album_cover = models.ImageField(upload_to='events/gallery/collection')
    uploaded_time = models.DateTimeField(null=True, blank=True, editable=True)
    is_processing = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)

    def get_faces(self):
        return CroppedGalleryFace.objects.filter(album=self.pk)

    class Meta:
        db_table = 'event_gallery_image'


class CroppedGalleryFace(models.Model):
    gallery_image = models.ForeignKey(GalleryImage, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/gallery/faces/')
    face_locations = models.JSONField(default=None, blank=True, null=True)
    face_embedding = models.JSONField(default=None, blank=True, null=True)
    parent_face = models.ForeignKey('CroppedGalleryFace', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'event_gallery_image_face'


class UserSelfieRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=128)
    mobile_number = models.CharField(max_length=24)
    email_id = models.CharField(max_length=256, default=None, blank=True, null=True)
    selfie_image = models.ImageField(upload_to='user_selfies')
    selfie_embedding = models.JSONField(default=None, blank=True, null=True)
    last_matching = models.DateTimeField(null=True, blank=True, editable=True)
    created_at = models.DateTimeField(default=timezone.now, editable=True)

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'event_user_selfie_registration'
