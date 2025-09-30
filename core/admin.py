from django.contrib import admin
from .models import Category, Produce, Customer, Order, OrderItem, Testimonial, Media, ProduceImage, NutritionInfo, HealthBenefit

# -------------------------
# Category Admin
# -------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    list_filter = ['name']
    ordering = ['name']

# -------------------------
# Produce Admin
# -------------------------
@admin.register(Produce)
class ProduceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity', 'available', 'is_organic', 'rating', 'review_count']
    list_filter = ['category', 'available', 'seasonal', 'is_organic']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock_quantity', 'available', 'is_organic']
    ordering = ['name']
    actions = ['mark_as_available', 'mark_as_unavailable']

    def mark_as_available(self, request, queryset):
        queryset.update(available=True)
    mark_as_available.short_description = "Mark selected products as available"

    def mark_as_unavailable(self, request, queryset):
        queryset.update(available=False)
    mark_as_unavailable.short_description = "Mark selected products as unavailable"

# -------------------------
# Customer Admin
# -------------------------
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number']  # removed 'is_business'
    search_fields = ['name', 'email', 'phone_number']
    ordering = ['name']

# -------------------------
# Order Admin
# -------------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ['price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'order_date', 'status', 'total_price']
    list_filter = ['status', 'order_date']
    search_fields = ['customer__name']
    inlines = [OrderItemInline]
    list_editable = ['status']
    ordering = ['-order_date']

# -------------------------
# OrderItem Admin
# -------------------------
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'produce', 'quantity', 'price']
    search_fields = ['produce__name']
    list_filter = ['order']
    ordering = ['order']

# -------------------------
# Testimonial Admin
# -------------------------
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['get_customer_name', 'produce', 'rating', 'created_at']
    search_fields = ['customer__name', 'comment']
    list_filter = ['rating', 'created_at', 'produce']
    ordering = ['-created_at']

    def get_customer_name(self, obj):
        return obj.customer.name
    get_customer_name.short_description = "Customer"

# -------------------------
# Media Admin
# -------------------------
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'description']  # removed non-existent fields
    search_fields = ['title', 'description']
    ordering = ['title']

# -------------------------
# ProduceImage Admin
# -------------------------
@admin.register(ProduceImage)
class ProduceImageAdmin(admin.ModelAdmin):
    list_display = ['produce', 'image', 'alt_text']
    search_fields = ['produce__name', 'alt_text']
    ordering = ['produce']

# -------------------------
# NutritionInfo Admin
# -------------------------
@admin.register(NutritionInfo)
class NutritionInfoAdmin(admin.ModelAdmin):
    list_display = ['produce', 'name', 'value']
    search_fields = ['produce__name', 'name', 'value']
    ordering = ['produce']

# -------------------------
# HealthBenefit Admin
# -------------------------
@admin.register(HealthBenefit)
class HealthBenefitAdmin(admin.ModelAdmin):
    list_display = ['produce', 'description']
    search_fields = ['produce__name', 'description']
    ordering = ['produce']
