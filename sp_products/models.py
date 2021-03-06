from django.db import models
from django.utils import timezone
import pytz


class SpProduct(models.Model):
    sp_id = models.CharField(max_length=255, default='')
    title = models.CharField(max_length=255, default='')
    formatted_price = models.CharField(max_length=255, default='')
    formatted_msrp = models.CharField(max_length=255, default='')
    image_cover_thumb_url = models.TextField(default='')
    image_cover_url = models.TextField(default='')
    listing_category_id = models.CharField(max_length=255, default='')
    category_name = models.CharField(max_length=255, default='')
    collection_ids = models.CharField(max_length=255, default='')
    price_min_cents = models.FloatField(default=0.0)
    price_max_cents = models.FloatField(default=0.0)
    country_origin = models.CharField(max_length=255, default='')
    shipping_exclusions = models.TextField(default='')
    shipping_specific_countries = models.TextField(default='')
    shipping_countries = models.TextField(default='')
    ships_internationally = models.BooleanField(default=False)
    state_origin = models.CharField(max_length=255, default='')
    sp_tags = models.CharField(max_length=255, default='')
    supplier_shop_name = models.CharField(max_length=255, default='')
    trending_until = models.CharField(max_length=255, default='')
    premium = models.BooleanField(default=False)
    best_selling = models.BooleanField(default=False)
    location = models.CharField(max_length=255, default='')
    activated_at = models.CharField(max_length=255, default='')
    is_customizable = models.BooleanField(default=False)
    is_handmade = models.BooleanField(default=False)
    is_ethically_sourced = models.BooleanField(default=False)
    total_inventory = models.IntegerField(default=0)
    manufacturer_origin_country = models.CharField(max_length=255, default='')
    percentage_from_retail_to_best_price = models.IntegerField(default=0)
    percentage_from_base_to_best_price = models.IntegerField(default=0)
    is_discounted = models.BooleanField(default=False)
    formatted_slashed_price = models.CharField(max_length=255, default='')
    pushed_count = models.IntegerField(default=0)
    free_usa_shipping = models.BooleanField(default=False)
    is_fav = models.BooleanField(default=False)
    ships_from_us = models.BooleanField(default=False)
    us_delivery_time_min = models.IntegerField(default=0)
    us_delivery_time_max = models.IntegerField(default=0)
    us_shipping_price_cents = models.FloatField(default=0.0)
    us_shipping_price_formatted = models.CharField(default='', max_length=254)

    def __str__(self):
        return str(self.pushed_count) + ' - ' + self.title

class SpDailyInv(models.Model):
    sp_id = models.CharField(max_length=255, default='')
    total_inventory = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now(), blank=False)

    def __str__(self):
        return str(self.date) + ' - ' + str(self.total_inventory)

# SP DAILY SALES RECORD
class SpPrDailySale(models.Model):
	date = models.DateField(default=timezone.now())
	quantitySold = models.IntegerField(default=0)
	sp_id = models.CharField(max_length=255, default='')

	def __str__(self):
		return self.sp_id + ' - ' + str(self.quantitySold)
