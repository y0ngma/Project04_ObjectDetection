from django.urls import path
from . import views

urlpatterns = [
    path('stream/', views.stream, name="stream"),
    path('service/', views.service, name="sevice"),
    path('caps/', views.caps, name="caps"),
]