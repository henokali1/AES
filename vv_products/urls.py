from django.urls import path
from . import views


urlpatterns = [
    path('all/', views.vv_product_all, name='vv_product_all.html'),
]