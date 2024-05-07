from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from users.permissions import Administrator, AdministratorOrManager


class ListOrdersAPIView(APIView):
    permission_classes = [Administrator]

    def get(self, request):
        order_by = request.query_params.get("order_by", "date")
        orders = Orders.objects.all().order_by(order_by)
        is_approved_orders = request.query_params.get("approved_orders", False)

        if is_approved_orders:
            orders = orders.objects.filter(is_approved=True)
        elif is_approved_orders is False:
            orders = orders.objects.filter(is_approved=False)

        serialized_info = OrdersSerializer(orders, many=True)
        return Response(serialized_info.data)

    def delete(self):
        pass


class DetailOrderAPIView(APIView):
    permission_classes = [Administrator]

    def get_order(self, pk):
        try:
            return Orders.objects.get(pk=pk)
        except Orders.DoesNotExist:
            print("Order Does Not Exist")

    def get(self, request, pk):
        order = self.get_order(pk)
        serialized_info = OrdersSerializer(order)
        return Response(serialized_info.data)

    def patch(self, request, pk):
        order = self.get_order(pk)
        serialized_update = OrdersSerializer(order, data=request.data, partial=True)
        if serialized_update.is_valid():
            serialized_update.save()
            return Response("Order was updated successfully")
        return Response("Failed Order Update")

    def delete(self, request, pk):
        self.get_order(pk).delete()
        return Response("Order Was Deleted Successfully")

    def post(self, request, pk):
        order = self.get_order(pk)
        action = request.query_params.get("action", None)
        if action == "checkLicenceStatus":
            return self.checkLicenceStatus()
        elif action == "generateInvoice":
            return self.generateInvoice()

    def checkLicenceStatus(self):
        pass

    def generateInvoice(self):
        pass


class CreateOrderAPIView(APIView):
    permission_classes = [AdministratorOrManager]

    def post(self, request):
        new_order = OrdersSerializer(Orders, data=request.data)
        if new_order.is_valid():
            new_order.save(is_approved=False)
            return Response("New Order have been created")
        return Response("Failed Order creation")


class ListInvoicesAPIView(APIView):
    permission_classes = [Administrator]

    def get(self, request):
        order_by = request.query_params.get("order_by", "date")
        invoices = Invoices.objects.all().order_by(order_by)
        serialized_info = InvoicesSerializer(invoices, many=True)
        return Response(serialized_info.data)

    def post(self, request):
        pass

    def sendEmail(self):
        pass

    def deleteInvoices(self):
        pass


class DetailInvoiceAPIView(APIView):
    permission_classes = [Administrator]

    def get_invoice(self, pk):
        try:
            return Invoices.objects.get(pk=pk)
        except Invoices.DoesNotExist:
            print("Order Does Not Exist")

    def get(self, request, pk):
        invoice = self.get_invoice(pk)
        serialized_info = OrdersSerializer(invoice)
        return Response(serialized_info.data)

    def patch(self, request, pk):
        invoice = self.get_invoice(pk)
        serialized_update = InvoicesSerializer(invoice, data=request.data, partial=True)
        if serialized_update.is_valid():
            serialized_update.save()
            return Response("invoice was updated successfully")
        return Response("Failed invoice Update")

    def delete(self, request, pk):
        self.get_invoice(pk).delete()
        return Response("invoice Was Deleted Successfully")

    def post(self, request, pk):
        action = request.query_params.get("action", None)
        if action == "pdfPrint":
            return self.pdfPrint()
        elif action == "pdfOpen":
            return self.pdfOpen()

    def pdfPrint(self):
        pass

    def pdfOpen(self):
        pass

