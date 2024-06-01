from django.http import FileResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from users.permissions import Administrator, AdministratorOrManager
from .tasks import *
from .generate_codes_order import generate_code
from .models import *
from email_sender.views import SendEmailAPIView
from utils.cache_logic import *


class ListOrdersAPIView(APIView):
    permission_classes = [Administrator]

    def get(self, request):
        order_by = request.query_params.get("order_by", "date_creating")
        is_approved_orders = request.query_params.get("approved_orders", False)

        orders = get_set_cache(
            queryset=Orders.objects.all().order_by(order_by).prefetch_related('user', 'customer'),
            serializer=OrdersSerializer,
            cache_name=ORDERS_LIST_CACHE_NAME,
            type_data='list'
        )
        if is_approved_orders:
            orders = orders.filter(is_approved=True)
        elif is_approved_orders is False:
            orders = orders.filter(is_approved=False)

        return Response(orders)

    def delete(self, request):
        orders_id_list = request.data.get('orders_for_delete', [])

        if not orders_id_list:
            return Response("Not corrected orders list")

        orders = Orders.objects.fillter(id__in=orders_id_list)

        if not orders.exists():
            return Response("The orders now exist")

        orders.delete()
        cache.delete(ORDER_DETAIL_CACHE_NAME)
        cache.delete(ORDERS_LIST_CACHE_NAME)

        return Response("The Orders was successfully deleted")


class DetailOrderAPIView(APIView):
    permission_classes = [Administrator]

    def get_order(self, pk):
        try:
            return Orders.objects.get(pk=pk)
        except Orders.DoesNotExist:
            print("Order Does Not Exist")

    def get(self, request, pk):
        result = get_set_cache(
            queryset=self.get_order(pk),
            serializer=OrdersSerializer,
            cache_name=ORDER_DETAIL_CACHE_NAME,
            type_data='detail'
        )
        return Response(result)

    def patch(self, request, pk):
        order = self.get_order(pk)
        serialized_update = OrdersSerializer(order, data=request.data, partial=True)
        if serialized_update.is_valid():
            serialized_update.save()
            cache.delete(ORDER_DETAIL_CACHE_NAME)
            cache.delete(ORDERS_LIST_CACHE_NAME)
            return Response("Order was updated successfully")
        return Response("Failed Order Update")

    def delete(self, request, pk):
        self.get_order(pk).delete()
        cache.delete(ORDER_DETAIL_CACHE_NAME)
        cache.delete(ORDERS_LIST_CACHE_NAME)
        return Response("Order Was Deleted Successfully")

    def post(self, request, pk):
        order = self.get_order(pk)
        action = request.query_params.get("action", None)
        if action == "checkLicenceStatus":
            return check_licence_status.delay()


class CreateOrderAPIView(APIView):
    permission_classes = [AdministratorOrManager]

    def post(self, request):
        new_order = OrdersSerializer(data=request.data)

        if new_order.is_valid():
            new_order.save(is_approved=False)
            cache.delete(ORDERS_LIST_CACHE_NAME)

            return Response("New Order have been created")
        return Response(new_order.errors, status=400)


class CreateInvoiceAPIView(APIView):
    permission_classes = [Administrator]

    def post(self, request, pk_order):
        order = Orders.objects.get(pk=pk_order)
        codes_list = generate_code(pk_order)

        new_invoice = Invoices(
            code_invoice=codes_list[0],
            code_order_invoice=codes_list[1],
            date=order.delivery_date,
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
        queryset = Invoices.objects.all().order_by(order_by)
        result = get_set_cache(
            queryset=queryset,
            serializer=InvoicesSerializer,
            cache_name=INVOICES_LIST_CACHE_NAME,
            type_data='list'
        )
        return Response(result)

    def post(self, request):
        # send the email to selected
        invoices_id_list = request.data.get('invoices_to_mail', [])

        sender = SendEmailAPIView.as_view()
        email_response = sender(request=request)

        for invoice_id in invoices_id_list:
            try:
                invoice = Invoices.objects.get(id=invoice_id)
                invoice.is_sent_mail = True
                invoice.save()
            except Invoices.DoesNotExist:
                return Response("The invoice don't exist")

    def delete(self, request):
        invoices_id_list = request.data.get('invoices_for_delete', [])

        if not invoices_id_list:
            return Response("Not corrected invoices list")

        invoices = Invoices.objects.fillter(id__in=invoices_id_list)

        if not invoices.exists():
            return Response("The invoices now exist")

        invoices.delete()
        return Response("The Invoices was successfully deleted")


class DetailInvoiceAPIView(APIView):
    permission_classes = [Administrator]

    def get_invoice(self, pk):
        try:
            return Invoices.objects.get(pk=pk)
        except Invoices.DoesNotExist:
            print("Order Does Not Exist")

    def get(self, request, pk):
        result = get_set_cache(
            queryset=self.get_invoice(pk),
            serializer=InvoicesSerializer,
            cache_name=INVOICE_DETAIL_CACHE_NAME,
            type_data='detail'
        )
        return Response(result)

    def patch(self, request, pk):
        invoice = self.get_invoice(pk)
        serialized_update = InvoicesSerializer(invoice, data=request.data, partial=True)
        if serialized_update.is_valid():
            serialized_update.save()
            cache.delete(INVOICES_LIST_CACHE_NAME)
            cache.delete(INVOICE_DETAIL_CACHE_NAME)
            return Response("invoice was updated successfully")
        return Response("Failed invoice Update")

    def delete(self, request, pk):
        self.get_invoice(pk).delete()
        cache.delete(INVOICES_LIST_CACHE_NAME)
        cache.delete(INVOICE_DETAIL_CACHE_NAME)
        return Response("invoice Was Deleted Successfully")

    def post(self, request, pk):
        action = request.query_params.get("action", None)
        if action == "pdfOpen":
            return self.pdfOpen(pk)

    def pdfOpen(self, pk):
        file_path = ''
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')


class GeneratePDFDoc(APIView):
    permission_classes = [Administrator]

    def get(self, request, pk_invoice, type_pdf):
        invoice = Invoices.objects.get(pk=pk_invoice)
        serialized_invoice = InvoicesSerializer(invoice)
        context = {'invoice': serialized_invoice.data}

        if type_pdf == 'order_invoice':
            context['code'] = serialized_invoice.data.code_order_invoice
        elif type_pdf == 'invoice':
            context['code'] = serialized_invoice.data.code_invoice

        generate_invoice.delay(context)
        return Response("The invoice pdf generation is started")

