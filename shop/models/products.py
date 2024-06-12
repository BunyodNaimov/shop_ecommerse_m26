from django.db import models
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_discount = models.PositiveIntegerField(help_text="скидка", default=0)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.price}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        product = Product.objects.filter(slug=self.slug).first()
        if product:
            raise ValidationError(f"Продукт '{self.title}' уже существует")
        super(Product, self).save(*args, **kwargs)


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    attribute_name = models.CharField(help_text="Attribute Name", max_length=255)
    attribute_value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.attribute_name} - {self.attribute_value}"

    class Meta:
        unique_together = (("product", "attribute_name", "attribute_value"),)


class ProductImage(models.Model):
    """
    Поле is_primary предназначено для указания того,
    какое из изображений является основным или главным для данного продукта.
    """
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/")
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.product.title


class ProductVariation(models.Model):
    """
    ProductVariation - для хранения различных конфигураций продуктов с соответствующими ценами:
    """
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="variations")
    variation = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.title} - {self.variation}"

    class Meta:
        unique_together = (("product", "variation"),)


class ProductColor(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="colors")
    color = models.CharField(max_length=255)
    hex_code = models.CharField(max_length=7)
