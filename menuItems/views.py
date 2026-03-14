from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from menuItems.models import MenuItem
from menuItems.serializers import MenuItemSerializer
from user.permissions import IsCEO


class ListCreateMenuItemView(ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsCEO()]
        return [AllowAny()]


class RetrieveUpdateDeleteMenuItemView(RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsCEO()]
        return [AllowAny()]


class PublicMenuItemListView(ListAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [AllowAny]