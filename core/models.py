from django.db import models

# -------------------------
# Produce / Products
# -------------------------
class Produce(models.Model):
    CATEGORY_CHOICES = [
        ('fruit', 'Fruit'),
        ('nut', 'Nut'),
        ('dairy', 'Dairy'),
        ('root', 'Root/Tuber'),
        ('vegetable', 'Vegetable'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seasonal = models.BooleanField(default=True)
    stock_quantity = models.IntegerField()
    image = models.ImageField(upload_to='produce/')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# -------------------------
# Customers
# -------------------------
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    is_business = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# -------------------------
# Orders
# -------------------------
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    delivery_address = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"

# Linking orders to produce
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # store price at time of order

    def __str__(self):
        return f"{self.quantity} x {self.produce.name}"

# -------------------------
# Customer Testimonials
# -------------------------
class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.rating}⭐"

# -------------------------
# Media (images/videos)
# -------------------------
# -------------------------
# Media (images/videos) — for dynamic gallery
# -------------------------
class Media(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    title = models.CharField(max_length=100)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='media/')  # Stores uploaded image/video
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.media_type})"



