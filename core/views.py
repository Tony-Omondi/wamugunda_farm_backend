from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProduceSerializer, OrderSerializer, TestimonialSerializer, MediaSerializer
from .models import Produce, Testimonial, Media


# -------------------------
# Static farm info
# -------------------------


# -------------------------
# Produce
# -------------------------
@api_view(['GET'])
def produce_list(request):
    produce = Produce.objects.filter(available=True)
    serializer = ProduceSerializer(produce, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def produce_detail(request, pk):
    produce = Produce.objects.get(id=pk)
    serializer = ProduceSerializer(produce)
    return Response(serializer.data)

# -------------------------
# Orders
# -------------------------
@api_view(['POST'])
def order_create(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()
        return Response(OrderSerializer(order).data)
    return Response(serializer.errors, status=400)

# -------------------------
# Testimonials
# -------------------------
@api_view(['GET'])
def testimonial_list(request):
    testimonials = Testimonial.objects.all()
    serializer = TestimonialSerializer(testimonials, many=True)
    return Response(serializer.data)

# -------------------------
# Media
# -------------------------
@api_view(['GET'])
def media_list(request):
    media = Media.objects.all().order_by('-uploaded_at')  # newest first
    serializer = MediaSerializer(media, many=True)
    return Response(serializer.data)

