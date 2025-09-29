from django.urls import path
from . import views

urlpatterns = [


    # Produce
    path('produce/', views.produce_list, name='produce-list'),
    path('produce/<int:pk>/', views.produce_detail, name='produce-detail'),

    # Orders
    path('orders/', views.order_create, name='order-create'),

    # Testimonials
    path('testimonials/', views.testimonial_list, name='testimonial-list'),

    # Media
    path('media/', views.media_list, name='media-list'),
]
