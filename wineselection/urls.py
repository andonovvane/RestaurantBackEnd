from django.urls import path

from wineselection.views import RetrieveUpdateDeleteWineView, PublicWineListView

urlpatterns = [
    path('', PublicWineListView.as_view()),
    path('<int:pk>/', RetrieveUpdateDeleteWineView.as_view())
]