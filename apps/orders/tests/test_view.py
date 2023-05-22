from unittest.mock import patch

from django.contrib.auth.models import User as UserDjango
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.orders.models import Orders


class UserTestCase(TestCase):
    def setUp(self):
        self.user_django = UserDjango.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.order_1 = Orders.objects.create(
            user_id=1,
            item_description="Teste 1",
            item_quantity=0,
            item_price=0,
            total_value=0,
        )
        self.order_2 = Orders.objects.create(
            user_id=1,
            item_description="Teste 1",
            item_quantity=0,
            item_price=0,
            total_value=0,
        )
        self.client = APIClient()
        self.client_not_authorization = APIClient()
        self.client.force_authenticate(user=self.user_django)

    def test_order_list(self):
        url = reverse("order-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 2)

    def test_create_order(self):
        new_user_data = {
            "user_id": 1,
            "item_description": "Teste 1",
            "item_quantity": 0,
            "item_price": 0,
            "total_value": 0,
        }
        url = reverse("order-list")
        response = self.client.post(url, data=new_user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Orders.objects.count(), 3)

        created_order = Orders.objects.get(
            id=3
        )

        self.assertEqual(created_order.item_description,
                         new_user_data["item_description"])
        self.assertEqual(created_order.user_id, new_user_data["user_id"])
        self.assertEqual(created_order.item_quantity,
                         new_user_data["item_quantity"])
        self.assertEqual(created_order.item_price, new_user_data["item_price"])
        self.assertEqual(created_order.total_value,
                         new_user_data["total_value"])

        response_data = response.json()
        self.assertEqual(
            response_data["item_description"],
            new_user_data["item_description"]
        )
        self.assertEqual(
            response_data["user_id"],
            new_user_data["user_id"]
        )
        self.assertEqual(
            response_data["item_quantity"], new_user_data["item_quantity"])
        self.assertEqual(response_data["item_price"],
                         new_user_data["item_price"])
        self.assertEqual(response_data["total_value"],
                         new_user_data["total_value"])

    def test_retrieve_order(self):
        url = reverse("order-detail", args=[self.order_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["user_id"], self.order_1.user_id)
        self.assertEqual(
            response_data["item_description"], self.order_1.item_description)
        self.assertEqual(
            response_data["item_quantity"], self.order_1.item_quantity)
        self.assertEqual(response_data["item_price"], self.order_1.item_price)
        self.assertEqual(
            response_data["total_value"], self.order_1.total_value)

    def test_update_order(self):
        url = reverse("order-detail", args=[self.order_1.id])

        valid_data = {
            "user_id": 1,
            "item_description": "Teste Update",
            "item_quantity": 0,
            "item_price": 0,
            "total_value": 0,
        }

        response = self.client.patch(url, data=valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        url = reverse("order-detail", args=[self.order_1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_order_with_invalid_data(self):
        invalid_data = {
            "user_id": [],
            "item_description": [],
            "item_quantity": -1,
            "item_price": -2,
            "total_value": -3,
        }

        url = reverse("order-list")
        response = self.client.post(url, data=invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                'item_description': ['This field is required.'],
                'item_price':
                ['Ensure this value is greater than or equal to 0.0.'],
                'item_quantity':
                ['Ensure this value is greater than or equal to 0.'],
                'total_value':
                ['Ensure this value is greater than or equal to 0.0.'],
                'user_id': ['This field is required.']
            }
        )

    def test_retrieve_nonexistent_order(self):
        url = reverse("order-detail", args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_order_with_invalid_data(self):
        url = reverse("order-detail", args=[self.order_1.id])

        invalid_data = {
            "user_id": [],
            "item_description": [],
            "item_quantity": -1,
            "item_price": -2,
            "total_value": -3,
        }

        response = self.client.patch(url, data=invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                'item_quantity':
                ['Ensure this value is greater than or equal to 0.'],
                'item_price':
                ['Ensure this value is greater than or equal to 0.0.'],
                'total_value':
                ['Ensure this value is greater than or equal to 0.0.']
            }
        )

    def test_delete_nonexistent_order(self):
        url = reverse("order-detail", args=[9999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_without_authorization(self):
        url = reverse("order-detail", args=[9999])
        response = self.client_not_authorization.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_without_authorization(self):
        url = reverse("order-detail", args=[self.order_1.id])
        response = self.client_not_authorization.patch(url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_without_authorization(self):
        url = reverse("order-detail", args=[self.order_1.id])
        response = self.client_not_authorization.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_without_authorization(self):
        url = reverse("order-list")
        response = self.client_not_authorization.post(url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_orders_by_cpf(self):
        with patch('common.user_api.UserAPI.filter_user_by_cpf') as mock:
            mock.return_value = {
                "count": 1,
                "results": [{'id': 1}]
            }
            url = reverse("order-list")
            response = self.client.get(f"{url}?cpf=123")

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data["results"]), 2)
