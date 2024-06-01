from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.permissions import *
from .serializers import *
from .models import *
from rest_framework import viewsets
from utils.cache_logic import *


class ListProductsWithoutPriceAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Product.objects.all()
        result = get_set_cache(
            queryset=queryset,
            serializer=ProductsWithoutPriceSerializer,
            cache_name=PRODUCTS_LIST_CACHE_NAME,
            type_data='list'

        )
        return Response(result)


class ListProductsWithPriceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Product.objects.all()
        result = get_set_cache(
            queryset=queryset,
            serializer=ProductsWithPriceSerializer,
            cache_name=PRODUCT_DETAIL_CACHE_NAME,
            type_data='list'
        )
        return Response(result)


class AddNewProductAPIView(APIView):
    permission_classes = [Administrator]

    def post(self, request):
        new_serialized_product = ProductsWithPriceSerializer(Product, data=request.data)
        if new_serialized_product.is_valid():
            new_serialized_product.save()
            cache.delete(PRODUCTS_LIST_CACHE_NAME)
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
        result = get_set_cache(
            queryset=self.get_product(pk),
            serializer=ProductsWithPriceSerializer,
            cache_name=PRODUCT_DETAIL_CACHE_NAME,
            type_data='detail'
        )
        return Response(result)

    def patch(self, request, pk):
        serialized_update = ProductsWithPriceSerializer(self.get_product(pk), data=request.data, partial=True)
        if serialized_update.is_valid():
            serialized_update.save()
            cache.delete(PRODUCTS_LIST_CACHE_NAME)
            cache.delete(PRODUCT_DETAIL_CACHE_NAME)
            return Response("Was update successfully")
        return Response("Fail in updating")

    def delete(self, request, pk):
        self.get_product(pk).delete()
        cache.delete(PRODUCTS_LIST_CACHE_NAME)
        cache.delete(PRODUCT_DETAIL_CACHE_NAME)
        return Response("Was delete successfully")


# adding states, country's, etc.
def create_viewset(model, serializer):
    class GenericViewSet(viewsets.ModelViewSet):
        queryset = model.objects.all()
        serializer_class = serializer
        permission_classes = [AdministratorOrManager]

    return GenericViewSet


CountryViewSet = create_viewset(Country, CountrySerializer)
RegionViewSet = create_viewset(Region, RegionSerializer)
BeverageViewSet = create_viewset(Beverage, BeverageSerializer)
StateViewSet = create_viewset(State, StateSerializer)
StockProductViewSet = create_viewset(StockProduct, StockProductSerializer)
CodeProductViewSet = create_viewset(CodeProduct, CodeProductSerializer)
PriceProductViewSet = create_viewset(PriceProduct, PriceProductSerializer)

