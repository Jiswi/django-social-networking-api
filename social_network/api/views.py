from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import models
from django.shortcuts import render, redirect
from rest_framework import generics, permissions
from .forms import CustomUserCreationForm, CustomAuthenticationForm
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


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Update 'home' with the URL name of your home page
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            print(user)
            login(request, user)
            return redirect('home')  # Update 'home' with the URL name of your home page
        else:
            print(form.errors)
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm


@login_required
def home(request):
    return render(request, 'home.html')
