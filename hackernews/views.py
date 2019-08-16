from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Item
from .serializers import ItemSerializer


class ListsPost(GenericViewSet):
    queryset = Item.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = ItemSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)
