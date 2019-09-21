from django.urls import path
from . import views


urlpatterns = [
    path('', views.pages, name='dashboard.html'),
    path('all-categories/', views.all_categories, name='all-categories.html'),
    path('cats/<str:cat_urls>/', views.cat_urls, name='cat_urls.html'),
]