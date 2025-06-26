from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from ingredients.models import Ingredient
from ingredients.serializers import IngredientSerializer

class ListCreateIngredientView(ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class RetrieveUpdateDeleteIngredientView(RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]