from django.urls import path

from userprofile.views import ListCreateProfileAPIView, RetrieveUpdateDestroyProfileAPIView

urlpatterns = [
    path('', ListCreateProfileAPIView.as_view()),
    path('<int:pk>/', RetrieveUpdateDestroyProfileAPIView.as_view()),
]
