from django.contrib.auth import login

from django.core.mail import send_mail
from django.urls import reverse_lazy

from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm
from users.models import User


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        send_mail(
            subject="Добро пожаловать в наш сервис",
            message="Спасибо, что зарегистрировались в нашем сервисе!",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)

