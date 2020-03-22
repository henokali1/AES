from django.urls import path
from . import views


urlpatterns = [
    path('', views.fbads, name='dashboard.html'),
    path('all', views.all_ads, name='all-ads.html'),
]