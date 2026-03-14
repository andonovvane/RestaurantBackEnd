from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from ingredients.models import Ingredient
from ingredients.serializers import IngredientSerializer
from user.permissions import IsCEO, IsStaff


class ListCreateIngredientView(ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsCEO()]
        return [IsStaff()]


class RetrieveUpdateDeleteIngredientView(RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsCEO()]
        return [IsStaff()]