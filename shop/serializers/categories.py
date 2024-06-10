from rest_framework import serializers

from shop.models.categories import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "icon", "parent")
        read_only_fields = ("id", "slug", "icon",)
