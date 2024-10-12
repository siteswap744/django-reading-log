#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.views.generic import CreateView
from django.urls import path
from .forms import CustomUserCreationForm
from .views import MyLoginView

urlpatterns = [
    path('signup/', CreateView.as_view(
        template_name='accounts/signup.html',
        #form_class=UserCreationForm,
        form_class=CustomUserCreationForm,
        success_url='/',
    ), name='signup'),
    path('login/', MyLoginView.as_view(
        redirect_authenticated_user=True,
        template_name='accounts/login.html'
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
