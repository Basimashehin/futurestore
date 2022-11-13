from rest_framework import serializers
from owner.models import Products,Categories,Carts,Orders,Reviews


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(read_only=True)
    class Meta:
        model = Products
        fields = "__all__"
    def create(self, validated_data):
        category = self.context.get("category")
        return Products.objects.create(**validated_data,category=category)

class CartSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    product=serializers.CharField(read_only=True)
    created_date=serializers.DateTimeField(read_only=True)
    status=serializers.CharField(read_only=True)
    class Meta:
        model=Carts
        fields="__all__"

    def create(self, validated_data):
        user=self.context.get("user")
        product=self.context.get("product")
        return Carts.objects.create(**validated_data,user=user,product=product)

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    product = serializers.CharField(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)
    expected_delivery_date = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Orders
        fields = "__all__"

    def create(self, validated_data):
        user=self.context.get("user")
        product=self.context.get("product")
        return Orders.objects.create(**validated_data,user=user,product=product,status="order_placed")
class ReviewSerializers(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    product = serializers.CharField(read_only=True)
    class Meta:
        model = Reviews
        fields = "__all__"



