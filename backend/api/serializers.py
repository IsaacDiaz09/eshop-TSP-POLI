from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from .models import Category, Product, ProductVariant, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password_confirm')

    def validate(self, attrs):
        if 'password' in attrs:
            password = attrs['password']
            password_confirm = attrs.get('password_confirm')
            if not password_confirm:
                raise serializers.ValidationError({"password_confirm": ["Este campo es requerido."]})
            if password != password_confirm:
                raise serializers.ValidationError({"password_confirm": ["Las contraseñas no coinciden."]})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductVariantSerializer(serializers.ModelSerializer):
    size_display = serializers.CharField(source='get_size_display', read_only=True)

    class Meta:
        model = ProductVariant
        fields = ('id', 'size', 'size_display', 'color', 'stock')

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'brand', 'category', 'price', 'description', 'image_url', 'variants')

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    brand = serializers.CharField(source='product.brand', read_only=True)
    size = serializers.CharField(source='variant.size', read_only=True)
    color = serializers.CharField(source='variant.color', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'brand', 'variant', 'size', 'color', 'quantity', 'price')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'total_price', 'status', 'status_display', 'created_at', 'items')
        read_only_fields = ('total_price', 'status')

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        
        # Raw items data is passed from the view, or we can look at context data
        items_data = self.context.get('items', [])
        if not items_data:
            raise serializers.ValidationError("El carrito de compras no puede estar vacío.")

        # Create Order first
        order = Order.objects.create(
            user=user,
            total_price=0, # Will calculate and update
            status='Completed' # Complete simulated order directly
        )

        total_price = 0
        for item_data in items_data:
            variant_id = item_data.get('variant_id')
            quantity = int(item_data.get('quantity', 1))

            try:
                variant = ProductVariant.objects.select_for_update().get(id=variant_id)
            except ProductVariant.DoesNotExist:
                raise serializers.ValidationError(f"La variante de producto #{variant_id} no existe.")

            if variant.stock < quantity:
                raise serializers.ValidationError(
                    f"Stock insuficiente para {variant.product.name} ({variant.size} - {variant.color}). "
                    f"Disponible: {variant.stock}, Solicitado: {quantity}."
                )

            # Deduct stock
            variant.stock -= quantity
            variant.save()

            # Calculate price
            price = variant.product.price
            item_total = price * quantity
            total_price += item_total

            # Create order item
            OrderItem.objects.create(
                order=order,
                product=variant.product,
                variant=variant,
                quantity=quantity,
                price=price
            )

        # Update total price of the order
        order.total_price = total_price
        order.save()

        return order
