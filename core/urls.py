from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list, name='category_list'),
    path('produce/', views.produce_list, name='produce_list'),
    path('produce/<int:pk>/', views.produce_detail, name='produce_detail'),
    path('orders/', views.order_create, name='order_create'),
    path('testimonials/', views.testimonial_list, name='testimonial_list'),
    path('media/', views.media_list, name='media_list'),
]