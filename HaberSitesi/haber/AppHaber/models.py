from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title

class HaberSites(models.Model):
    title = models.CharField(max_length=150, verbose_name="Haber Sitesi Adı")
    categorys = models.ManyToManyField(Category)

    def __str__(self):
        return self.title
