from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from events.models import Event, GalleryImage, Gallery


@login_required
def dashboard(request):
    events = Event.objects.all().order_by('-pk')[:3]
    report = {
        'event_count': Event.objects.filter(user=request.user).count(),
        'gallery_count': Gallery.objects.filter(event__user=request.user).count(),
        'image_count': GalleryImage.objects.filter(gallery__event__user=request.user).count()
    }
    return render(request, 'dashboard/dashboard.html', {'events': events, 'report': report})


@login_required
def coming_soon(request):
    return render(request, 'dashboard/coming_soon.html')
