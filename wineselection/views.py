from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from wineselection.models import Wine
from wineselection.serializers import WineSerializer

class ListCreateWineView(ListCreateAPIView):
    queryset = Wine.objects.all()
    serializer_class = WineSerializer

class RetrieveUpdateDeleteWineView(RetrieveUpdateDestroyAPIView):
    queryset = Wine.objects.all()
    serializer_class = WineSerializer

class PublicWineListView(ListAPIView):
    queryset = Wine.objects.all()
    serializer_class = WineSerializer
    permission_classes = [AllowAny]