from django.db import models

# CATEGORIE URL'S
class CategorieUrls(models.Model):
    url = models.CharField(max_length=250, default="")

    def __str__(self):
        return str(self.pk) + ' - ' + self.url
