from django.db import models
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ProduceImage(models.Model):
    produce = models.ForeignKey('Produce', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='produce/images/')
    alt_text = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Image for {self.produce.name}"

class NutritionInfo(models.Model):
    produce = models.ForeignKey('Produce', on_delete=models.CASCADE, related_name='nutrition')
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}: {self.value} for {self.produce.name}"

class HealthBenefit(models.Model):
    produce = models.ForeignKey('Produce', on_delete=models.CASCADE, related_name='benefits')
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.description} for {self.produce.name}"

class Produce(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seasonal = models.BooleanField(default=True)
    stock_quantity = models.IntegerField()
    image = models.ImageField(upload_to='produce/')
    available = models.BooleanField(default=True)
    badge = models.CharField(max_length=50, blank=True, null=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    delivery_time = models.CharField(max_length=50, blank=True, null=True)
    is_organic = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)
    review_count = models.IntegerField(default=0)
    details = models.TextField(blank=True, null=True)
    storage_tips = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def update_rating(self):
        testimonials = Testimonial.objects.filter(produce=self)
        if testimonials.exists():
            self.rating = testimonials.aggregate(Avg('rating'))['rating__avg']
            self.review_count = testimonials.count()
            self.save()

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Order {self.id} by {self.customer.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.produce.name} in Order {self.order.id}"

class Testimonial(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE)
    rating = models.FloatField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.produce.name} ({self.rating})"

class Media(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title