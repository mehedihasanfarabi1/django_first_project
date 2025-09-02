from django.db import models
from django.utils.text import slugify

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='productss/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
