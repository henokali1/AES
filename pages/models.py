from django.db import models
from django.utils import timezone

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

	def __str__(self):
		return str(self.pk) + ' - ' + self.productId + ' - ' + str(self.totSalesCount)
