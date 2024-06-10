from rest_framework import serializers, validators

from shop.models.products import ProductAttribute


class ProductAttributeListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ("id", "product", "attribute_name", "attribute_value")
        read_only_fields = ("id", "product")
        # validators = [validators.UniqueTogetherValidator(
        #     queryset=ProductAttribute.objects.all(),
        #     fields=("product", "attribute_name", "attribute_name"),
        #     message="Этот аттрибут уже есть!"
        # )]

    # def validate(self, attrs):
    #     product_id = self.context['request'].parser_context['kwargs'].get('product_id')
    #     print(f'product_id: {product_id}')
    #     attrs['product'] = product_id
    #     return attrs
    #
    # def create(self, validated_data):
    #     product_id = self.context['request'].parser_context['kwargs'].get('product_id')
    #     if product_id:
    #         validated_data['product'] = product_id
    #     return super().create(validated_data)
