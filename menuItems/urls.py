from django.urls import path

from menuItems.views import RetrieveUpdateDeleteMenuItemView, PublicMenuItemListView

urlpatterns = [
    path('', PublicMenuItemListView.as_view()),
    path('<int:pk>/', RetrieveUpdateDeleteMenuItemView.as_view())
]