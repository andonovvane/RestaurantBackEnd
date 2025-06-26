from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from menuItems.models import MenuItem
from menuItems.serilizers import MenuItemSerializer

class ListCreateMenuItemView(ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

class RetrieveUpdateDeleteMenuItemView(RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]