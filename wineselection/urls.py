from django.urls import path

from wineselection.views import ListCreateWineView, RetrieveUpdateDeleteWineView

urlpatterns = [
    path('', ListCreateWineView.as_view()),
    path('<int:pk>/', RetrieveUpdateDeleteWineView.as_view())
]