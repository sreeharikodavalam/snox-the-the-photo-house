from django.urls import path
from .views import coming_soon, dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('comingsoon', coming_soon, name='coming_soon'),
]
