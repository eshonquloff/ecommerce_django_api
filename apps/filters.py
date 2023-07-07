from django_filters import FilterSet, NumberFilter

from apps.models import Product


class CustomProductFilter(FilterSet):
    _from = NumberFilter(field_name='price', lookup_expr='gte')
    _to = NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['title', 'brand__name', '_from', '_to']
    #     fields = {
    #         'price': ['gte', 'lte'] # bu oddiy from to kabi chiroyli chiqmaydi, sodda korinishda chiqadi
    # }
