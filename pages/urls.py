from django.urls import path
from . import views


urlpatterns = [
    path('', views.pages, name='dashboard.html'),
    path('local-server-add-product/<str:prds>/', views.local_server_add_product, name='local-server-add-product.html'),
    path('daily-sales-filter/', views.daily_sales_filter, name='daily-sales-filter.html'),
    path('product-filter/', views.product_filter, name='product-filter.html'),
    path('most-profitable/', views.most_profitable, name='most-profitable.html'),
    path('update-cookie/<str:cookie>/', views.update_cookie, name='update-cookie.html'),
    path('update-daily-sales-record/', views.update_daily_sales_record, name='update-daily-sales-record.html'),
    path('all-categories/', views.all_categories, name='all-categories.html'),
    path('products-srtd-order-count/', views.products_srtd_order, name='products_srtd_order.html'),
    path('save-products/<str:products>/', views.save_products, name='save_products.html'),
    path('cats/<str:cat_urls>/', views.cat_urls, name='cat_urls.html'),
    path('fbads', views.fbads, name='fbads.html'),
]