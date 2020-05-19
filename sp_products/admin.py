from django.contrib import admin
from .models import *

admin.site.site_header = 'SYS Administration'
admin.site.site_title = "Admin Portal"


admin.site.register(SpProduct)
admin.site.register(SpDailyInv)
admin.site.register(SpPrDailySale)
