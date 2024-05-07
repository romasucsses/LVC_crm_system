from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Customer
from .serializers import CustomerSerializerAPI
from users.permissions import *



class ListCustomersAPIView(APIView):
    permission_classes = [AdministratorOrManager]

    def get(self, request):
        order_by = request.query_params.get("order_by", "name")
        customers = Customer.objects.all().order_by(order_by)
        return Response(CustomerSerializerAPI(customers, many=True).data)

    # updating feature like: last call, last visit, last testing, last order
    def patch(self, request):
        customer = Customer.objects.get(pk=request.data.get("id"))
        new_info = CustomerSerializerAPI(customer, data=request.data, partial=True)
        if new_info.is_valid():
            new_info.save()
            return Response("successfully done")
        return Response("got fail")


class DetailCustomerAPIView(APIView):
    permission_classes = [Administrator]

    def get_customer(self, pk):
        return Customer.objects.get(pk=pk)

    def get(self, request, pk):
        serialized_info = CustomerSerializerAPI(self.get_customer(pk))
        return Response(serialized_info.data)

    def patch(self, request, pk):
        serialized_info = CustomerSerializerAPI(self.get_customer(pk), data=request.data, partial=True)
        if serialized_info.is_valid():
            serialized_info.save()
            return Response("Was updated successfully")
        return Response("Was Failed")

    def delete(self, request, pk):
        self.get_customer(pk).delete()
        return Response("Was deleted successfully")


class AddNewCustomerAPIView(APIView):
    permission_classes = [Administrator]

    def post(self, request):
        new_customer_serialized = CustomerSerializerAPI(Customer, data=request.data)
        if new_customer_serialized.is_valid():
            new_customer_serialized.save()
            return Response("New customer was successfully added")
        return Response("Failed adding of new customer")


class SendEmailAPIView(APIView):
    permission_classes = [Administrator]

    def post(self, request):
        sending_to = request.query_params.get("sending_to")
        if sending_to == "to_all":
            self.sendingToAllCustomers()
        elif sending_to == "to_selected":
            self.sendingToSelectedCustomers()

    def sendingToAllCustomers(self):
        pass

    def sendingToSelectedCustomers(self):
        pass
