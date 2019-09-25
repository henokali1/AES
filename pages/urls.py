from django.urls import path
from . import views


urlpatterns = [
    path('', views.pages, name='dashboard.html'),
    path('analyze/', views.analyze, name='analyze.html'),
    path('update-cookie/<str:cookie>/', views.update_cookie, name='update-cookie.html'),
    path('update-daily-sales-record/', views.update_daily_sales_record, name='update-daily-sales-record.html'),
    path('all-categories/', views.all_categories, name='all-categories.html'),
    path('products-srtd-order-count/', views.products_srtd_order, name='products_srtd_order.html'),
    path('save-products/<str:products>/', views.save_products, name='save_products.html'),
    path('cats/<str:cat_urls>/', views.cat_urls, name='cat_urls.html'),
]