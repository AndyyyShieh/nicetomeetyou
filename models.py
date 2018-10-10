from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=20)
    link = models.CharField(max_length=50)

    def __str__(self):
        return self.title
