from django.urls import path
from .views import detect_colors

urlpatterns = [
    path('detect_colors/', detect_colors, name='detect_colors'),
]
