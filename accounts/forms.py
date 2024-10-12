from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import User as CustomUser


class CustomUserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = CustomUser
