from django.db import models


class EventTypes(models.Model):
    event_type_name = models.CharField(max_length=64)
    separation = models.CharField(max_length=6)
    names_count = models.SmallIntegerField()


class Event(models.Model):
    event_type = models.OneToOneField(EventTypes, on_delete=models.CASCADE, default=1)
    bride_name = models.CharField(max_length=64, default='')
    groom_name = models.CharField(max_length=64, default='')
    date = models.DateField(default=None)
    venue = models.CharField(max_length=64, default='')
    note = models.CharField(max_length=512, default='')
    cover_image = models.ImageField(upload_to='events/cover', default='')

    def title(self):
        return f"{self.groom_name} {self.event_type.separation} {self.bride_name}"

    def __str__(self):
        return self.title()


# class EventNames(models.Model):
#     event = models.OneToOneField(Event, on_delete=models.CASCADE)
#     name = models.CharField(max_length=64)


class Gallery(models.Model):
    name = models.CharField(max_length=32)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    album_cover = models.ImageField(upload_to='events/gallery/collection')
    uploaded_time = models.DateTimeField(null=True)
    is_processing = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)

    def get_faces(self):
        return CroppedGalleryFace.objects.filter(album=self.pk)


class CroppedGalleryFace(models.Model):
    album = models.ForeignKey(GalleryImage, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/gallery/faces/')
    face_locations = models.JSONField(default=None, blank=True, null=True)
    face_embedding = models.JSONField(default=None, blank=True, null=True)


class UserSelfieRegistration(models.Model):
    user_name = models.CharField(max_length=128)
    mobile_number = models.CharField(max_length=24)
    email_id = models.CharField(max_length=256, default=None, blank=True, null=True)
    selfie_image = models.ImageField(upload_to='user_selfies')
    selfie_embedding = models.JSONField(default=None, blank=True, null=True)
