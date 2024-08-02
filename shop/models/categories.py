from sqlite3 import IntegrityError

from django.db import models
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError
from unidecode import unidecode

from shop.utils import custom_slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to='icon_category/', null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Генерируем slug из названия категории
        self.slug = custom_slugify(self.name)

        # Проверяем, существует ли категория с таким же slug и это не текущая категория
        existing_category = Category.objects.filter(slug=self.slug).exclude(id=self.id).first()
        if existing_category:
            raise ValidationError(f"Категория с названием '{self.name}' уже существует.")

        super(Category, self).save(*args, **kwargs)
