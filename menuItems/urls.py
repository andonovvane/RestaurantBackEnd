from django.urls import path

from menuItems.views import ListCreateMenuItemView, RetrieveUpdateDeleteMenuItemView

urlpatterns = [
    path('', ListCreateMenuItemView.as_view()),
    path('<int:pk>/', RetrieveUpdateDeleteMenuItemView.as_view())
]