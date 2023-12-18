from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from events.models import Event


@login_required
def dashboard(request):
    events = Event.objects.all()
    return render(request, 'dashboard/dashboard.html', {'events': events})


@login_required
def coming_soon(request):
    return render(request, 'dashboard/coming_soon.html')
