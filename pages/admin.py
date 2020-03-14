from django.contrib import admin
from .models import *

admin.site.site_header = 'SYS Administration'
admin.site.site_title = "Admin Portal"


admin.site.register(CategorieUrl)
admin.site.register(Product)
admin.site.register(DailySale)
admin.site.register(Cookie)
admin.site.register(Err)
admin.site.register(Ad)