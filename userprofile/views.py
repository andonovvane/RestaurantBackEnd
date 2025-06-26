from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from userprofile.models import UserProfile
from userprofile.serializers import UserProfileSerializer


class ListCreateProfileAPIView(ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveUpdateDestroyProfileAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
