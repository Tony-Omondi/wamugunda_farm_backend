from rest_framework import serializers
from .models import Category, Produce, ProduceImage, NutritionInfo, HealthBenefit, Customer, Order, OrderItem, Testimonial, Media

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProduceImageSerializer(serializers.ModelSerializer):
    # Rename 'image' to 'url' and 'alt_text' to 'alt' to match frontend expectations
    url = serializers.ImageField(source='image', read_only=True)
    alt = serializers.CharField(source='alt_text', read_only=True)
    
    class Meta:
        model = ProduceImage
        fields = ['id', 'url', 'alt']

class NutritionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionInfo
        fields = ['id', 'name', 'value']

class HealthBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthBenefit
        fields = ['id', 'description']

class ProduceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    images = ProduceImageSerializer(many=True, read_only=True)
    nutrition = NutritionInfoSerializer(many=True, read_only=True)
    benefits = HealthBenefitSerializer(many=True, read_only=True)
    # Ensure primary image field returns absolute URL
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Produce
        fields = [
            'id', 'name', 'category', 'category_id', 'description', 'price', 'seasonal',
            'stock_quantity', 'image', 'available', 'badge', 'original_price',
            'delivery_time', 'is_organic', 'rating', 'review_count', 'details',
            'storage_tips', 'images', 'nutrition', 'benefits'
        ]

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone_number']

class OrderItemSerializer(serializers.ModelSerializer):
    produce = ProduceSerializer(read_only=True)
    produce_id = serializers.PrimaryKeyRelatedField(
        queryset=Produce.objects.all(), source='produce', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'produce', 'produce_id', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True
    )

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_id', 'order_date', 'total_price', 'status', 'items']

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must have at least one item.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if items_data is not None:
            instance.items.all().delete()  # Clear existing items
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)
        return instance

class TestimonialSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    produce = ProduceSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True
    )
    produce_id = serializers.PrimaryKeyRelatedField(
        queryset=Produce.objects.all(), source='produce', write_only=True
    )

    class Meta:
        model = Testimonial
        fields = ['id', 'customer', 'customer_id', 'produce', 'produce_id', 'rating', 'comment', 'created_at']

class MediaSerializer(serializers.ModelSerializer):
    # Rename fields to match MediaGallery expectations
    url = serializers.ImageField(source='image', read_only=True)
    alt = serializers.CharField(source='title', read_only=True)
    caption = serializers.CharField(source='description', read_only=True, allow_null=True)

    class Meta:
        model = Media
        fields = ['id', 'title', 'url', 'alt', 'caption', 'description']