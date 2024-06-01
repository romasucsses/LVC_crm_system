from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Customer
from .serializers import CustomerSerializerAPI
from users.permissions import *
from utils.cache_logic import *


class ListCustomersAPIView(APIView):
    permission_classes = [AdministratorOrManager]

    def get(self, request):
        order_by = request.query_params.get("order_by", "name")
        queryset = Customer.objects.all().order_by(order_by)
        result = get_set_cache(
            queryset=queryset,
            serializer=CustomerSerializerAPI,
            cache_name=CUSTOMERS_LIST_CACHE_NAME,
            type_data='list'
        )
        return Response(result)


class UpdateCustomerAPIView(APIView):
    permission_classes = [Administrator]

    def patch(self, request, pk_customer):
        customer = Customer.objects.get(pk=pk_customer)
        new_info = CustomerSerializerAPI(customer, data=request.data, partial=True)
        if new_info.is_valid():
            new_info.save()
            cache.delete(CUSTOMERS_LIST_CACHE_NAME)
            cache.delete(CUSTOMER_DETAIL_CACHE_NAME)
            return Response("successfully done")
        return Response("got fail")


class DetailCustomerAPIView(APIView):
    permission_classes = [Administrator]

    def get_customer(self, pk):
        return Customer.objects.get(pk=pk)

    def get(self, request, pk):
        result = get_set_cache(
            queryset=self.get_customer(pk),
            serializer=CustomerSerializerAPI,
            cache_name=CUSTOMER_DETAIL_CACHE_NAME,
            type_data='detail'
        )
        return Response(result)

    def delete(self, request, pk):
        self.get_customer(pk).delete()
        cache.delete(CUSTOMERS_LIST_CACHE_NAME)
        cache.delete(CUSTOMER_DETAIL_CACHE_NAME)
        return Response("Was deleted successfully")


class AddNewCustomerAPIView(APIView):
    permission_classes = [Administrator]

    def post(self, request):
        new_customer_serialized = CustomerSerializerAPI(data=request.data)
        if new_customer_serialized.is_valid():
            new_customer_serialized.save()
            cache.delete(CUSTOMERS_LIST_CACHE_NAME)
            return Response("New customer was successfully added")
        return Response("Failed adding of new customer")

