from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer, ProduceSerializer, OrderSerializer, TestimonialSerializer, MediaSerializer
from .models import Category, Produce, Testimonial, Media

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
        return Response({'error': 'Product not found'}, status=404)

@api_view(['POST'])
def order_create(request):
    serializer = OrderSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

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