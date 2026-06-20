from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Category, Product, ProductVariant, Order
from .serializers import UserSerializer, CategorySerializer, ProductSerializer, OrderSerializer

class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Usuario registrado exitosamente.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Product.objects.all().prefetch_related('variants', 'category').order_by('id')
        
        # Basic search (by name or brand)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(brand__icontains=search) |
                Q(description__icontains=search)
            )

        # Advanced filters
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        brand = self.request.query_params.get('brand', None)
        if brand:
            queryset = queryset.filter(brand__iexact=brand)

        size = self.request.query_params.get('size', None)
        if size:
            queryset = queryset.filter(variants__size=size).distinct()

        min_price = self.request.query_params.get('min_price', None)
        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except ValueError:
                pass

        max_price = self.request.query_params.get('max_price', None)
        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except ValueError:
                pass

        return queryset

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Users can only see their own orders
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product', 'items__variant').order_index_by('-created_at') if hasattr(Order.objects, 'order_index_by') else Order.objects.filter(user=self.request.user).prefetch_related('items__product', 'items__variant').order_by('-created_at')

    def create(self, request, *args, **kwargs):
        # We extract the cart items from the request body
        items_data = request.data.get('items', [])
        
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request, 'items': items_data}
        )
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
