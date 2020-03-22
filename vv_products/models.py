from django.db import models

# vv product
class VvProduct(models.Model):
    vvpk = models.IntegerField(default=0)
    title = models.CharField(max_length=250, default='')
    category = models.CharField(max_length=250, default='')
    timestamp = models.CharField(max_length=250, default='')
    description = models.TextField(default='')
    fb_targeting = models.CharField(max_length=250, default='')
    cogs = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    profit = models.FloatField(default=0.0)
    favorite = models.BooleanField(default=False)
    fb_url = models.TextField(default='')
    likes = models.FloatField(default=0.0)
    comments = models.FloatField(default=0.0)
    redirects = models.FloatField(default=0.0)
    aliexpress1 = models.TextField(default='')
    aliexpress2 = models.TextField(default='')
    amazon1 = models.TextField(default=None)
    amazon2 = models.TextField(default=None)
    competitor_store = models.TextField(default='')
    aliexpress_data = models.TextField(default='')
    images = models.TextField(default='')
    ad_creative = models.TextField(default='')

    def __str__(self):
        return str(self.pk) + ' - ' + self.title
