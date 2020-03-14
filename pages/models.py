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
	shippingCountries = models.CharField(max_length=250, default="")
	stockAvailable = models.IntegerField(default=0.0)
	storeRating = models.FloatField(default=0.0)
	productListingHasVideo = models.BooleanField(default=False)
	
	imageUrl = models.URLField(default='')
	logisticsReliability = models.CharField(max_length=100, default="")
	sellerDsSupplier = models.BooleanField(default=False)
	storeUrl = models.URLField(default='')
	avgDailySale = models.FloatField(default=0.0)
	dailySaleVariance = models.FloatField(default=11111.0)

	shippingPrice = models.FloatField(default=0.0)
	shippingCompany = models.CharField(max_length=250, default="")
	commitDay = models.IntegerField(default=0)
	estimatedDeliveryDayMin = models.IntegerField(default=0)
	estimatedDeliveryDayMax = models.IntegerField(default=0)
	trackingAvailable = models.BooleanField(default=False)

	nums = models.FloatField(default=0.0)

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

# ERRORS
class Err(models.Model):
	productId = models.CharField(max_length=250, default="")
	file_name = models.CharField(max_length=250, default="")
	func_name = models.CharField(max_length=250, default="")
	err = models.TextField(default='')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.productId) + ' - ' + str(self.func_name)

# FB Ads
class Ad(models.Model):
	countryStats = models.TextField(default='')
	genderStats = models.TextField(default='')
	ageStats = models.TextField(default='')
	asy_id = models.TextField(default='')
	isIg = models.TextField(default='')
	text = models.TextField(default='')
	createdOn = models.TextField(default='')
	privacyScope = models.TextField(default='')
	minAge = models.TextField(default='')
	maxAge = models.TextField(default='')
	actor = models.TextField(default='')
	countries = models.TextField(default='')
	genders = models.TextField(default='')
	snapshot = models.TextField(default='')
	attachments = models.TextField(default='')
	comments = models.TextField(default='')
	adType = models.TextField(default='')
	linkToAd = models.TextField(default='')
	mainAttachment = models.TextField(default='')
	height = models.TextField(default='')
	likeNum = models.TextField(default='')
	commentsNum = models.TextField(default='')
	shareNum = models.TextField(default='')

	def __str__(self):
		return str(self.pk) + ' - ' + str(self.likeNum)

