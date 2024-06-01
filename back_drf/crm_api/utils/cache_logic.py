from django.core.cache import cache

PRODUCTS_LIST_CACHE_NAME = 'products_list_cache_data'
PRODUCT_DETAIL_CACHE_NAME = 'product_detail_cache_data'

CUSTOMERS_LIST_CACHE_NAME = 'customers_list_cache_data'
CUSTOMER_DETAIL_CACHE_NAME = 'customer_detail_cache_data'

ORDERS_LIST_CACHE_NAME = 'orders_list_cache_data'
ORDER_DETAIL_CACHE_NAME = 'order_detail_cache_data'

INVOICES_LIST_CACHE_NAME = 'invoices_list_cache_data'
INVOICE_DETAIL_CACHE_NAME = 'invoice_detail_cache_data'

USERS_LIST_CACHE_NAME = 'users_list_cache_data'
USER_DETAIL_CACHE_NAME = 'user_detail_cache_data'

CACHE_DURATIONS = (60 * 60) * 15  # 15h


def get_set_cache(queryset, serializer, cache_name: str, type_data: str):
    exist_cache = cache.get(cache_name)

    if exist_cache:
        return exist_cache
    else:
        data = queryset
        if type_data == 'list':
            new_cache = serializer(data, many=True).data
        elif type_data == 'detail':
            new_cache = serializer(data).data

        cache.set(cache_name, new_cache, CACHE_DURATIONS)
        return new_cache
