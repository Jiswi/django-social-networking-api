from django.db import models
from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserSerializer


# Create your views here.
class UserSearchAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        keyword = self.request.query_params.get('q', '')
        return CustomUser.objects.filter(
            models.Q(email__iexact=keyword) |
            models.Q(username__icontains=keyword)
        ).exclude(id=self.request.user.id)
