import uuid
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from snoxpro.settings import BASE_URL
from whatsapp.models import WhatsappLogSharedPhoto
from whatsapp.utils.send_welcome_message import send_welcome_message
from .forms import EventForm, UserSelfieRegistrationForm
from .models import Event, Gallery, GalleryImage, UserSelfieRegistration
from .utils.face_detector import match_selfies_and_send
from .utils.gallery_upload_utils import do_upload_gallery_image
from .utils.gallery_image_utils import detect_and_crop_faces, get_face_embedding
import base64
from django.core.files.base import ContentFile


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            # Assign the logged-in user if not provided in the form
            if 'user' not in form.cleaned_data or not form.cleaned_data['user']:
                form.instance.user = request.user
                event = form.save()
                return redirect('list_gallery', event_id=event.pk)
            else:
                redirect('login')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})


@login_required
def edit_event(request, event_id=None):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('list_events')
    else:
        form = EventForm(instance=event)
    form.fields['cover_image'].required = False

    return render(request, 'events/edit_event.html', {'form': form, 'event_id': event_id})


@login_required
def list_events(request):
    events = Event.objects.all()
    return render(request, 'events/list_events.html', {'events': events})


@login_required
def list_galleries(request, event_id=None):
    event = get_object_or_404(Event, pk=event_id, user=request.user)
    galleries = Gallery.objects.filter(event=event_id)
    return render(request, 'events/list_gallery.html', {'galleries': galleries, 'event': event})


@login_required
def create_gallery(request, event_id=None):
    event = get_object_or_404(Event, pk=event_id, user=request.user)
    error_message = ''
    name = ''
    if request.method == 'POST':
        name = request.POST.get('gallery_name')
        if name is not None and len(name) > 4:
            gallery_exists = Gallery.objects.filter(event=event_id, name=name).exists()
            if not gallery_exists:
                new_gallery = Gallery.objects.create(name=name, event=event)
                return redirect('list_gallery_images', gallery_id=new_gallery.pk)
            else:
                error_message = f"Gallery {name} already exist in this event"
        else:
            error_message = f"{name} is very short"
    return render(request, 'events/create_gallery.html', {'event': event, 'error_message': error_message, 'name': name})


@login_required
def list_gallery_images(request, gallery_id=None):
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    gallery_images = GalleryImage.objects.filter(gallery=gallery)
    return render(request, 'events/list_gallery_images.html', {'gallery': gallery, 'gallery_images': gallery_images})


@login_required
def upload_gallery_image(request, gallery_id=None):
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    return render(request, 'events/upload_gallery_images.html', {'gallery': gallery})


@csrf_exempt
@login_required
def upload_gallery_image_process(request, gallery_id=None):
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    if request.method == 'POST':
        files = request.FILES.getlist('file')
        if not files:
            return JsonResponse({'error': 'No files provided'})
        # Uploading and do necessary resizing file
        upload_result = do_upload_gallery_image(files, gallery_id, request.user)
        for uploaded_files in upload_result:
            # crete & save model
            gallery_image = GalleryImage.objects.create(gallery=gallery, image=uploaded_files['image'], image_thumbnail=uploaded_files['thumbnail'], uploaded_time=timezone.now())
            # run face recognition utils
            detect_and_crop_faces(gallery_image)
        return JsonResponse({'message': 'Files uploaded successfully!', 'filenames': upload_result})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def selfie_register(request, event_id=None):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = UserSelfieRegistrationForm(request.POST)

        if form.is_valid():
            # Decode and save the base64-encoded image
            selfie_image_data = request.POST.get('selfie')
            if selfie_image_data:
                print("am here")
                unique_filename = f"selfie_{timezone.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"
                format, imgstr = selfie_image_data.split(';base64,')
                ext = format.split('/')[-1]
                filename = f"{unique_filename}.{ext}"
                data = ContentFile(base64.b64decode(imgstr), name=filename)
                form.instance.selfie_image = data

                # Get face embedding from the image
                face_embedding = get_face_embedding(data.read())
                if face_embedding:
                    form.instance.event = event
                    selfie_temp_data = form.save()
                    pk = selfie_temp_data.pk
                    selfie_temp_data.selfie_embedding = ",".join(map(str, face_embedding))
                    selfie_temp_data.save()
                    selfie_registration = UserSelfieRegistration.objects.get(pk=pk)
                    image_url = f"{BASE_URL}{event.cover_image.url}"
                    send_welcome_message(f'91{selfie_registration.mobile_number}', selfie_registration.user_name, event_name=f'The Wedding of {str(event)}', image_url=image_url)
                    match_selfies_and_send(selfie_registration.pk)
                    return render(request, 'events/selfie_register_result.html', {'event': event, 'selfie_registration': selfie_registration})

        return JsonResponse({'error': 'Can find your face in image'})
    else:
        form = UserSelfieRegistrationForm()
        return render(request, 'events/selfie_register.html', {'event': event, 'form': form})


def face_registration_list(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    faces = UserSelfieRegistration.objects.filter(event=event)
    return render(request, 'events/list_face_registrations.html', {'faces': faces, 'event': event})


def distributed_image_list(request, event_id, mobile_number):
    event = get_object_or_404(Event, pk=event_id)
    face = UserSelfieRegistration.objects.filter(mobile_number=mobile_number).first()
    shared_photos = WhatsappLogSharedPhoto.objects.filter(mobile_number=f"91{mobile_number}")
    # gallery_images = GalleryImage.objects.filter(id__in=[entry.gallery_image. for entry in log_entries])
    return render(request, 'events/list_distributed_gallery_images.html', {'face': face, 'shared_photos': shared_photos, 'event': event})
