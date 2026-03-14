from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

User = get_user_model()

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "table_id": user.table_id
        })

class QRLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        table_id = request.data.get("table_id")
        if not table_id:
            return Response({"error": "No table_id provided"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(
            username=f"table_{table_id}",
            defaults={
                "email": f"table_{table_id}@restaurant.local",
                "role": "client",
                "table_id": table_id
            }
        )

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "table_id": table_id,
            "role": user.role,
        })