from django.db import models
from django.utils import timezone
from datetime import datetime

# FB Ads
class Ad(models.Model):
	countryStats = models.TextField(default='')
	genderStats = models.TextField(default='')
	ageStats = models.TextField(default='')
	asy_id = models.CharField(max_length=250, default='')
	isIg = models.BooleanField(default=False)
	text = models.TextField(default='')
	createdOn = models.CharField(max_length=250, default='')
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
	likeNum = models.FloatField(default=0.0)
	commentsNum = models.FloatField(default=0.0)
	shareNum = models.FloatField(default=0.0)
	imageUrl = models.CharField(max_length=250, default='')
	hasVideo = models.BooleanField(default=False)
	videoUrl = models.CharField(default='', max_length=250)

	def __str__(self):
		return str(self.pk) + ' - ' + str(self.likeNum)

