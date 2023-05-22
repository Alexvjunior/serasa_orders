import asyncio

from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.filters import OrderFilter
from apps.orders.models import Orders
from apps.orders.serializers import OrdersSerializer
from apps.orders.services import OrderService


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    service = OrderService()
    basename = "user"
    serializer_class = OrdersSerializer
    queryset = Orders.objects.all()
    http_method_names = ["post", "patch", "get", "delete"]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('cpf', openapi.IN_QUERY,
                          description="Filtrar por cpf do usuário",
                          type=openapi.TYPE_STRING
                          ),
    ])
    def list(self, request, *args, **kwargs):
        user_id = None

        if self.service.is_valid_search_user_id(request.query_params):
            user_id = asyncio.run(self.service.get_user_id_by_cpf(
                request.query_params['cpf']))
            queryset = self.filter_queryset(
                self.get_queryset().filter(user_id=user_id))
        else:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TokenObtainView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        )
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "token": token.key,
                }
            )
        else:
            return Response(
                {"error": "Credenciais inválidas"},
                status=status.HTTP_401_UNAUTHORIZED
            )
