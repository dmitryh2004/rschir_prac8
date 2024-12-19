from django.shortcuts import redirect
from django.urls import reverse


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            # Определяем URL для страниц входа и регистрации
            excluded_paths = [reverse('login'), reverse('main'), reverse('about'), reverse('service_list')]

            # Если пользователь не авторизован и не пытается получить доступ к общедоступным страницам
            if request.path not in excluded_paths:
                return redirect('login')  # Перенаправляем на страницу входа

        response = self.get_response(request)
        return response