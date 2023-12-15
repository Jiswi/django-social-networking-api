from django.urls import path
from .views import UserSearchAPIView, signup, login_view, home, CustomLoginView

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    # Add URLs for other functionalities
    path('search/', UserSearchAPIView.as_view(), name='user-search'),
]
