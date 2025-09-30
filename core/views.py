# core/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer, ProduceSerializer, OrderSerializer, TestimonialSerializer, MediaSerializer, CustomerSerializer
from .models import Category, Produce, Testimonial, Media, Customer, Order, OrderItem, Transaction
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest
import json
from .mpesa import initiate_stk_push, query_stk_push

@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def produce_list(request):
    produce = Produce.objects.filter(available=True)
    serializer = ProduceSerializer(produce, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def produce_detail(request, pk):
    try:
        produce = Produce.objects.get(id=pk)
        serializer = ProduceSerializer(produce, context={'request': request})
        return Response(serializer.data)
    except Produce.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def order_create(request):
    serializer = OrderSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def testimonial_list(request):
    testimonials = Testimonial.objects.all()
    serializer = TestimonialSerializer(testimonials, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def media_list(request):
    media = Media.objects.all()
    serializer = MediaSerializer(media, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
def checkout_view(request):
    try:
        data = request.data
        cart_items = data.get('cart_items', [])
        customer_data = data.get('customer', {})
        total_amount = data.get('total_amount', 0)

        if not cart_items or not customer_data or not total_amount:
            return Response({'error': 'Missing required fields: cart_items, customer, or total_amount'}, status=status.HTTP_400_BAD_REQUEST)

        customer_serializer = CustomerSerializer(data=customer_data)
        if not customer_serializer.is_valid():
            return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        customer = customer_serializer.save()

        order_data = {
            'customer': customer,
            'total_price': total_amount,
            'items': [
                {'produce_id': item['id'], 'quantity': item['quantity'], 'price': item['price']}
                for item in cart_items
            ]
        }
        order_serializer = OrderSerializer(data=order_data, context={'request': request})
        if not order_serializer.is_valid():
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        order = order_serializer.save()

        phone = customer_data.get('phone_number')
        response = initiate_stk_push(phone, str(total_amount))
        if response.get("ResponseCode") == "0":
            order.checkout_request_id = response["CheckoutRequestID"]
            order.save()
            return Response({
                'checkout_request_id': response["CheckoutRequestID"],
                'order_id': order.id,
                'message': 'STK Push initiated. Please complete payment on your phone.'
            }, status=status.HTTP_200_OK)
        else:
            order.status = 'failed'
            order.save()
            return Response({
                'error': response.get('errorMessage', 'Failed to initiate STK Push.')
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def payment_callback(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST requests are allowed")

    try:
        callback_data = json.loads(request.body)
        result_code = callback_data["Body"]["stkCallback"]["ResultCode"]
        checkout_request_id = callback_data["Body"]["stkCallback"]["CheckoutRequestID"]

        try:
            order = Order.objects.get(checkout_request_id=checkout_request_id)
        except Order.DoesNotExist:
            return HttpResponseBadRequest("Order not found")

        if result_code == 0:
            metadata = callback_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]
            amount = next(item["Value"] for item in metadata if item["Name"] == "Amount")
            mpesa_code = next(item["Value"] for item in metadata if item["Name"] == "MpesaReceiptNumber")
            phone = next(item["Value"] for item in metadata if item["Name"] == "PhoneNumber")

            order.status = 'completed'
            order.save()

            Transaction.objects.create(
                amount=amount,
                checkout_id=checkout_request_id,
                mpesa_code=mpesa_code,
                phone_number=phone,
                status="Success"
            )
            return Response({"ResultCode": 0, "ResultDesc": "Payment successful"})
        else:
            order.status = 'failed'
            order.save()
            return Response({"ResultCode": result_code, "ResultDesc": "Payment failed"})

    except (json.JSONDecodeError, KeyError) as e:
        return HttpResponseBadRequest(f"Invalid request data: {str(e)}")

@api_view(['POST'])
def stk_status_view(request):
    try:
        data = json.loads(request.body)
        checkout_request_id = data.get('checkout_request_id')
        if not checkout_request_id:
            return Response({'error': 'CheckoutRequestID is required'}, status=status.HTTP_400_BAD_REQUEST)

        status_response = query_stk_push(checkout_request_id)
        return Response({"status": status_response})
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON body"}, status=status.HTTP_400_BAD_REQUEST)