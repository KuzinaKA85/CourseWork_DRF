from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from users.apps import UsersConfig


app_name = UsersConfig.name


urlpatterns = [
    # Получение токена (логин)
    path("login/",
         LoginView.as_view(template_name="login.html"),
         name="login"),
    # Выход (удаление токена)
    path(
        "logout/",
        LogoutView.as_view(template_name="logged_out.html"),
        name="logout",
    ),

]
