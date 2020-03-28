from django.urls import path
from . import views


urlpatterns = [
    path('all/', views.vv_product_all, name='vv_product_all.html'),
    path('<int:pk>/', views.vv_product, name='vv_product.html'),
    path('fav-all/', views.fav_all, name='fav_all.html'),
    path('fav/<int:pk>/<str:is_fav>/', views.fav),
]