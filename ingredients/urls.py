from django.urls import path

from ingredients.views import ListCreateIngredientView, RetrieveUpdateDeleteIngredientView


urlpatterns = [
    path('', ListCreateIngredientView.as_view()),
    path('<int:pk>/', RetrieveUpdateDeleteIngredientView.as_view())
]