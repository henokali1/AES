from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('vv-product/', include('vv_products.urls')),
    path('adspy/', include('adspy.urls')),
    path('fb/', include('fb.urls')),
    path('sp-product/', include('sp_products.urls')),
]
