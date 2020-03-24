from django.urls import path
from . import views


urlpatterns = [
    path('interests/', views.interests, name='interests.html'),
]