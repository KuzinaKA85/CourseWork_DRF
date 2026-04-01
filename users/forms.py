from django.contrib.auth.forms import UserCreationForm

# from catalog.mixins import ProductFormMixin
from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]
