from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import UserAuthForm
import logging

logger = logging.getLogger("logger_info")


class AuthView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logger.info(f"User is_authenticated - user: {request.user}, groups: {request.user.groups.all()}")
            return render(request, 'user_auth/_base.html')
        form = UserAuthForm()
        return render(request, "user_auth/login.html", {'form': form})

    def post(self, request):
        # Создаем объект формы с данными из POST-запроса
        form = UserAuthForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            logging.info(f"USER Data for authenticate: pass - {password}, username - {username}")
            # Аутентифицируем пользователя
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                logger.info(f"Login user - {user}")
                return redirect('client_stat:client_stat')
            else:
                # Добавляем сообщение об ошибке, если аутентификация не удалась
                logger.error(f"Неправильный логин или пароль")
                form.add_error(None, "Неправильный логин или пароль")

        context = {'form': form}
        return render(request, "user_auth/login.html", context)


class LogoutView(View):
    def get(self, request):
        logger.info(f"Logout user: {request.user}")
        logout(request)
        return redirect(reverse("user_auth:login"))
