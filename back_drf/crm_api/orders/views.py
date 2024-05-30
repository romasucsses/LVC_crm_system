from django.http import FileResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from users.permissions import Administrator, AdministratorOrManager
from .tasks import *
from .generate_code import generate_code
from .models import *


class ListOrdersAPIView(APIView):
    permission_classes = [Administrator]

    def get(self, request):
        order_by = request.query_params.get("order_by", "date_creating")
        orders = Orders.objects.all().order_by(order_by).prefetch_related('user', 'customer')
        is_approved_orders = request.query_params.get("approved_orders", False)

        if is_approved_orders:
            orders = orders.filter(is_approved=True)
        elif is_approved_orders is False:
            orders = orders.filter(is_approved=False)

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
            return check_licence_status.delay()


class CreateOrderAPIView(APIView):
    permission_classes = [Administrator]

    def post(self, request):
        new_order = OrdersSerializer(data=request.data)

        if new_order.is_valid():
            new_order.save(is_approved=False)

            return Response("New Order have been created")
        return Response(new_order.errors, status=400)


class CreateInvoiceAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk_order):
        order = Orders.objects.get(pk=pk_order)
        codes_list = generate_code(pk_order)

        new_invoice = Invoices(
            code_invoice=codes_list[0],
            code_order_invoice=codes_list[1],
            date=order.delivery_date,
            # customer=order.customer,
            cart_data=order.cart_data,
            total_cases=order.cases_number,
            total_sum=order.total_sum,
            past_due='30days',
            is_sent_mail=False,
            ship_via='warehouse',
            terms='30'
        )
        new_invoice.save()
        new_invoice.customer.set(order.customer.all())
        return Response('invoice have been created successfully')


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
            pass
        elif action == "pdfOpen":
            return self.pdfOpen(pk)

    def pdfOpen(self, pk):
        file_path = ''
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')


class GeneratePDFDoc(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk_invoice):
        invoice = Invoices.objects.get(pk=pk_invoice)
        serialized_invoice = InvoicesSerializer(invoice)
        context = {'invoice': serialized_invoice.data}
        generate_invoice.delay(context)
        return Response("the invoice pdf generation is started")

