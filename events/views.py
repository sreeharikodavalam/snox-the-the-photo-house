import uuid

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from whatsapp.utils.send_welcome_message import send_welcome_message
from .forms import EventForm, UserSelfieRegistrationForm
from .models import Event, Gallery, GalleryImage, UserSelfieRegistration
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


@login_required
@csrf_exempt
def upload_gallery_image_process(request, gallery_id=None):
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    if request.method == 'POST':
        files = request.FILES.getlist('file')
        if not files:
            return JsonResponse({'error': 'No files provided'})
        # Uploading and do necessary resizing file
        uploaded_files = do_upload_gallery_image(files, gallery_id)
        for uploaded_file in uploaded_files:
            # save model
            gallery_image = GalleryImage.objects.create(gallery=gallery, album_cover=uploaded_file, uploaded_time=timezone.now())
            gallery_image.save()
            # run face recognition utils
            detect_and_crop_faces(gallery_image)
        return JsonResponse({'message': 'Files uploaded successfully!', 'filenames': uploaded_files})
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
                    selfie_temp_data = form.save()
                    pk = selfie_temp_data.pk
                    selfie_temp_data.selfie_embedding = ",".join(map(str, face_embedding))
                    selfie_temp_data.save()
                    selfie_registration = UserSelfieRegistration.objects.get(pk=pk)
                    send_welcome_message(f'91{selfie_registration.mobile_number}', selfie_registration.user_name, event_name=f'The Wedding of {str(event)}')
                    return render(request, 'events/selfie_register_result.html', {'event': event, 'selfie_registration': selfie_registration})

        return JsonResponse({'error': 'Can find your face in image'})
    else:
        form = UserSelfieRegistrationForm()
        return render(request, 'events/selfie_register.html', {'event': event, 'form': form})
