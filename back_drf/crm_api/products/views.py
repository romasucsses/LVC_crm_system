from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.permissions import Administrator
from .serializers import *
from .models import Product


class ListProductsWithoutPriceAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        products = Product.objects.all()
        serialized_info = ProductsWithoutPriceSerializer(products, many=True)
        return Response(serialized_info.data)


class ListProductsWithPriceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pass


class ManageListProductsAPIView(APIView):
    permission_classes = [Administrator]

    def get(self, request):
        products = Product.objects.all()
        serialized_info = ProductsWithPriceSerializer(products, many=True)
        return Response(serialized_info.data)

    def post(self, request):
        new_serialized_product = ProductsWithPriceSerializer(Product, data=request.data)
        if new_serialized_product.is_valid():
            new_serialized_product.save()
            return Response("new product was successfully added")
        return Response("fail in adding new product")


class ManageDetailProductAPIView(APIView):
    permission_classes = [Administrator]

    def get_product(self, pk):
        try:
            product = Product.objects.get(pk=pk)
            return product
        except Product.DoesNotExist:
            print("product not existing")

    def get(self, request, pk):
        serialized_info = ProductsWithPriceSerializer(self.get_product(pk))
        return Response(serialized_info.data)

    def patch(self, request, pk):
        serialized_update = ProductsWithPriceSerializer(self.get_product(pk), data=request.data, partial=True)
        if serialized_update.is_valid():
            serialized_update.save()
            return Response("Was update successfully")
        return Response("Fail in updating")

    def delete(self, request, pk):
        self.get_product(pk).delete()
        return Response("Was delete successfully")
