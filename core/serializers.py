from rest_framework import serializers
from .models import Produce, Customer, Order, OrderItem, Testimonial, Media

# -------------------------
# Produce
# -------------------------
class ProduceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produce
        fields = '__all__'

# -------------------------
# Customer
# -------------------------
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

# -------------------------
# OrderItem
# -------------------------
class OrderItemSerializer(serializers.ModelSerializer):
    produce = ProduceSerializer(read_only=True)
    produce_id = serializers.PrimaryKeyRelatedField(
        queryset=Produce.objects.all(), source='produce', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'produce', 'produce_id', 'quantity', 'price']

# -------------------------
# Order
# -------------------------
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True
    )

    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'delivery_address', 'order_date', 'status', 'total_price', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        total = 0
        for item_data in items_data:
            produce = item_data['produce']
            quantity = item_data['quantity']
            price = produce.price * quantity
            total += price
            OrderItem.objects.create(order=order, produce=produce, quantity=quantity, price=price)
        order.total_price = total
        order.save()
        return order

# -------------------------
# Testimonial
# -------------------------
class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

# -------------------------
# Media (dynamic gallery)
# -------------------------
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'title', 'media_type', 'file', 'description', 'uploaded_at']
