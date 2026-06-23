from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Category, Product, ProductVariant, Order, OrderItem

class EShopAPITests(APITestCase):

    def setUp(self):
        # 1. Create categories
        self.calzado = Category.objects.create(name="Calzado", slug="calzado")
        self.tops = Category.objects.create(name="Ropa Superior", slug="ropa-superior")

        # 2. Create products
        self.product1 = Product.objects.create(
            name="Volt Runner X1",
            brand="Volt",
            category=self.calzado,
            price=120000.00,
            description="Tenis de running ultraligeros",
            image_url="http://example.com/image.jpg"
        )
        self.product2 = Product.objects.create(
            name="DryFit Alpha Tee",
            brand="Volt",
            category=self.tops,
            price=45000.00,
            description="Camiseta deportiva de microfibra",
            image_url="http://example.com/image2.jpg"
        )

        # 3. Create variants
        self.variant1 = ProductVariant.objects.create(
            product=self.product1,
            size="M",
            color="Negro",
            stock=10
        )
        self.variant2 = ProductVariant.objects.create(
            product=self.product1,
            size="S",
            color="Gris",
            stock=5
        )
        self.variant3 = ProductVariant.objects.create(
            product=self.product2,
            size="L",
            color="Azul",
            stock=0 # Out of stock
        )

        # 4. User data
        self.user_data = {
            "username": "testuser",
            "email": "test@volt.com",
            "password": "testpassword123"
        }
        self.user = User.objects.create_user(
            username=self.user_data["username"],
            email=self.user_data["email"],
            password=self.user_data["password"]
        )

    def test_user_registration(self):
        url = reverse('auth_register')
        data = {
            "username": "newuser",
            "email": "new@volt.com",
            "password": "newpassword123",
            "password_confirm": "newpassword123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_user_login(self):
        url = reverse('token_obtain_pair')
        data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_get_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_product_basic_search(self):
        url = reverse('product-list')
        response = self.client.get(url, {'search': 'Runner'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Volt Runner X1')

    def test_product_advanced_filters(self):
        url = reverse('product-list')
        
        # Filter by size M
        response = self.client.get(url, {'size': 'M'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Volt Runner X1')

        # Filter by category
        response = self.client.get(url, {'category': self.tops.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'DryFit Alpha Tee')

        # Filter by price range
        response = self.client.get(url, {'min_price': 50000, 'max_price': 150000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Volt Runner X1')

    def test_order_creation_success(self):
        # Obtain token
        login_url = reverse('token_obtain_pair')
        login_response = self.client.post(login_url, {
            "username": self.user_data["username"],
            "password": self.user_data["password"]
        }, format='json')
        token = login_response.data['access']
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        url = reverse('order-list')
        order_data = {
            "items": [
                {"variant_id": self.variant1.id, "quantity": 2},
                {"variant_id": self.variant2.id, "quantity": 1}
            ]
        }

        response = self.client.post(url, order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'Completed')
        
        # Total price check: (120000 * 2) + (120000 * 1) = 360000.00
        self.assertEqual(float(response.data['total_price']), 360000.00)

        # Check stock decrement
        self.variant1.refresh_from_db()
        self.variant2.refresh_from_db()
        self.assertEqual(self.variant1.stock, 8) # 10 - 2
        self.assertEqual(self.variant2.stock, 4) # 5 - 1

    def test_order_creation_insufficient_stock(self):
        login_url = reverse('token_obtain_pair')
        login_response = self.client.post(login_url, {
            "username": self.user_data["username"],
            "password": self.user_data["password"]
        }, format='json')
        token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        url = reverse('order-list')
        order_data = {
            "items": [
                {"variant_id": self.variant3.id, "quantity": 1} # stock is 0
            ]
        }

        response = self.client.post(url, order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Confirm stock didn't change
        self.variant3.refresh_from_db()
        self.assertEqual(self.variant3.stock, 0)
