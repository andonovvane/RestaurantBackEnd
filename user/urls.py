from django.urls import path

from user.views import UserProfileView, QRLoginView

urlpatterns = [
    path('', UserProfileView.as_view()),
    path('qr-login/', QRLoginView.as_view()),
]