from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from wineselection.models import Wine
from wineselection.serializers import WineSerializer
from user.permissions import IsCEO


class ListCreateWineView(ListCreateAPIView):
    queryset = Wine.objects.all()
    serializer_class = WineSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsCEO()]
        return [AllowAny()]


class RetrieveUpdateDeleteWineView(RetrieveUpdateDestroyAPIView):
    queryset = Wine.objects.all()
    serializer_class = WineSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsCEO()]
        return [AllowAny()]


class PublicWineListView(ListAPIView):
    queryset = Wine.objects.all()
    serializer_class = WineSerializer
    permission_classes = [AllowAny]