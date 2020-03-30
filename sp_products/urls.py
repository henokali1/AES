from django.urls import path
from . import views


urlpatterns = [
    path('all/', views.sp_products_all, name='sp_products_all.html'),
]