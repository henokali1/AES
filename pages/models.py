from django.db import models
from django.utils import timezone
from datetime import datetime

# CATEGORIE URL'S
class CategorieUrl(models.Model):
    url = models.CharField(max_length=250, default="")

    def __str__(self):
        return str(self.pk) + ' - ' + self.url

# PRODUCTS
class Product(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True) 
	productId = models.CharField(max_length=250, default="")
	rating = models.FloatField(default=0.0)
	productTitle = models.CharField(max_length=250, default="")
	minPrice = models.FloatField(default=0.0)
	maxPrice = models.FloatField(default=0.0)
	storeName = models.CharField(max_length=250, default="")
	totSalesCount = models.IntegerField(default=0.0)
	imageUrl = models.URLField(default='')
	logisticsReliability = models.CharField(max_length=100, default="")
	sellerDsSupplier = models.BooleanField(default=False)
	storeUrl = models.URLField(default='')
	avgDailySale = models.FloatField(default=0.0)
	dailySaleVariance = models.FloatField(default=11111.0)


	def __str__(self):
		return str(self.pk) + ' - ' + self.productId + ' - ' + str(self.totSalesCount)

# DAILY SALES RECORD
class DailySale(models.Model):
	date = models.DateField(default=datetime.now)
	quantitySold = models.IntegerField(default=0)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.pk) + ' - ' + str(self.quantitySold)

# CURRENT COOKIE
class Cookie(models.Model):
	cookie = models.TextField(default='')

	def __str__(self):
		return 'Current Cookie'
