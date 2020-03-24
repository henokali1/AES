from django.db import models

# FB Interest
class FbInterest(models.Model):
    name = models.CharField(max_length=254, default='')
    audience_size = models.BigIntegerField(default=0)
    path = models.TextField(default='')

    def __str__(self):
        return self.name + ' - ' + str(self.audience_size)
