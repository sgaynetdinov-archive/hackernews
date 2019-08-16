from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from .models import Item
from .pagination import HackerNewsPagination
from .serializers import ItemSerializer


class ListsPost(ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    pagination_class = HackerNewsPagination
