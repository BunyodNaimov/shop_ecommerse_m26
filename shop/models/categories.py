from sqlite3 import IntegrityError

from django.db import models
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to='icon_category/', null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        category = Category.objects.filter(slug=self.slug).first()
        if category:
            raise ValidationError(f"Категория '{self.name}' уже существует")
        super(Category, self).save(*args, **kwargs)
