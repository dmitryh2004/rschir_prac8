import os
import random

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from faker import Faker

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

from .forms import *
from .models import *

fake = Faker()

localizator = {
    "ru": {
        "user_create_success": "Новый пользователь добавлен.",
        "service_create_success": "Новая услуга добавлена.",
        "save_success": "Данные сохранены.",
        "user_delete_success": "Пользователь успешно удален.",
        "service_delete_success": "Услуга успешно удалена.",
        "service_title": "Название",
        "service_desc": "Описание",
        "service_cost": "Стоимость",
        "service_link": "Ссылка",
        "link": "ссылка",
        "service_page_title": "Список услуг",
        "service_page_header": "Список услуг",
        "back": "Назад",
        "to_mainpage": "На главную",
        "view_page_title": "Информация об услуге",
        "view_page_header": "Информация об услуге",
        "user_list_page_title": "[admin] Список пользователей",
        "user_list_page_header": "Список пользователей",
        "username": "Имя пользователя",
        "password_hash": "Хэш пароля",
        "actions": "Действия",
        "edit": "Редактировать",
        "delete": "Удалить",
        "its_you": "(Это вы)",
        "add_user": "Добавить пользователя",
        "to_service_list": "К редактированию услуг",
        "user_create_page_title": "[admin] Добавить пользователя",
        "user_create_page_header": "Добавить пользователя",
        "password": "Пароль",
        "save": "Сохранить",
        "user_update_page_title": "[admin] Редактирование пользователя",
        "user_update_page_header": "Редактирование пользователя",
        "new_password": "Новый пароль",
        "error": "Ошибка",
        "user_with": "пользователь с",
        "service_with": "услуга с",
        "user_delete_page_title": "[admin] Удаление пользователя",
        "user_delete_are_you_sure": "Вы действительно хотите удалить пользователя с именем",
        "service_list_page_title": "[admin] Список услуг",
        "service_list_page_header": "Список услуг",
        "add_service": "Добавить услугу",
        "to_user_list": "К редактированию пользователей",
        "service_create_page_title": "[admin] Добавить услугу",
        "service_create_page_header": "Добавление услуги",
        "service_update_page_title": "[admin] Редактирование услуги",
        "service_update_page_header": "Редактирование услуги",
        "service_delete_page_title": "[admin] Удаление услуги",
        "service_delete_are_you_sure": "Вы действительно хотите удалить услугу с названием",
        "admin_menu_page_title": "[admin] Меню",
        "admin_menu_page_header": "Меню администратора",
        "settings": "Настройки",
        "upload_pdf": "Выгрузить PDF",
        "download_pdf": "Управление PDF файлами",
        "settings_page_title": "[admin] Настройки",
        "settings_page_header": "Настройки",
        "dark_theme": "Темная тема",
        "select_language": "Выберите язык:",
        "text_scale": "Масштаб текста:",
        "to_admin_menu": "К меню администратора",
        "upload_pdf_page_title": "[admin] Выгрузить PDF",
        "upload_pdf_page_header": "Загрузите свой PDF",
        "choose_pdf": "Выберите PDF",
        "upload": "Загрузить",
        "error_only_pdf_accepted": "Ошибка: можно загрузить только .pdf файлы.",
        "error_file_already_exists": "Ошибка: файл с таким именем уже существует.",
        "error_file_too_big": "Ошибка: размер файла больше 5 МБ.",
        "file": "Файл",
        "uploaded": "загружен.",
        "upload_error": "Ошибка при загрузке файла.",
        "unexpected_server_error": "Непредвиденная ошибка сервера.",
        "download_pdf_page_title": "[admin] Ваши PDF-файлы",
        "download_pdf_page_header": "Ваши PDF-файлы",
        "no_pdfs": "У вас нет загруженных PDF-файлов",
        "filename": "Название файла",
        "size": "Размер",
        "download": "Скачать",
        "file_delete_success": "Файл удален успешно.",
        "file_delete_error": "Ошибка при удалении файла.",
        "file_delete_not_found": "Файл не найден.",
        "file_delete_not_selected": "Не выбран файл для удаления.",
        "generate_fixtures": "Сгенерировать фикстуры",
        "fixtures_generated": "фикстур сгенерировано.",
        "fixtures_erased": "Имеющиеся фикстуры были удалены.",
        "show_stats": "Показать статистику",
        "show_stats_page_title": "[admin] Статистика",
        "show_stats_page_header": "Статистика сайта",
        "customer_name": "Клиент",
        "amount": "Количество",
        "comment": "Комментарии",
        "stats_graph1_name": "Наличие комментариев в записях",
        "stats_graph2_name": "Число оказанных услуг клиенту",
        "stats_graph3_name": "Сумма, оставленная каждым клиентом",
        "logout": "Выйти"
    },
    "en": {
        "user_create_success": "A new user was created.",
        "service_create_success": "A new service was created.",
        "save_success": "Saved successfully.",
        "user_delete_success": "User was deleted successfully.",
        "service_delete_success": "Service was deleted successfully.",
        "service_title": "Title",
        "service_desc": "Description",
        "service_cost": "Cost",
        "service_link": "Link",
        "link": "link",
        "service_page_title": "Service list",
        "service_page_header": "Service list",
        "back": "Back",
        "to_mainpage": "To home page",
        "view_page_title": "Service info",
        "view_page_header": "Service info",
        "user_list_page_title": "[admin] User list",
        "user_list_page_header": "User list",
        "username": "Username",
        "password_hash": "Password hash",
        "actions": "Actions",
        "edit": "Edit",
        "delete": "Delete",
        "its_you": "(It's you)",
        "add_user": "Add user",
        "to_service_list": "To service editing",
        "user_create_page_title": "[admin] Add user",
        "user_create_page_header": "Add user",
        "password": "Password",
        "save": "Save",
        "user_update_page_title": "[admin] Update user",
        "user_update_page_header": "Update user",
        "new_password": "New password",
        "error": "Error",
        "user_with": "the user with",
        "service_with": "the service with",
        "user_delete_page_title": "[admin] Delete user",
        "user_delete_are_you_sure": "Are you sure want to delete user with name",
        "service_list_page_title": "[admin] Service list",
        "service_list_page_header": "Service list",
        "add_service": "Add service",
        "to_user_list": "To user editing",
        "service_create_page_title": "[admin] Create service",
        "service_create_page_header": "Create service",
        "service_update_page_title": "[admin] Update service",
        "service_update_page_header": "Update service",
        "service_delete_page_title": "[admin] Delete service",
        "service_delete_are_you_sure": "Are you sure want to delete service with title",
        "admin_menu_page_title": "[admin] Menu",
        "admin_menu_page_header": "Administrator's menu",
        "settings": "Settings",
        "upload_pdf": "Upload PDF",
        "download_pdf": "PDF files management",
        "settings_page_title": "[admin] Settings",
        "settings_page_header": "Settings",
        "dark_theme": "Dark theme",
        "select_language": "Select language:",
        "text_scale": "Text scale:",
        "to_admin_menu": "To administrator's menu",
        "upload_pdf_page_title": "[admin] Upload PDF",
        "upload_pdf_page_header": "Upload your PDF",
        "choose_pdf": "Select PDF",
        "upload": "Upload",
        "error_only_pdf_accepted": "Error: only .pdf files are accepted.",
        "error_file_already_exists": "Error: file with such name already exists.",
        "error_file_too_big": "Error: file is bigger than 5 MB.",
        "file": "File",
        "uploaded": "uploaded.",
        "upload_error": "Error while uploading file.",
        "unexpected_server_error": "Unexpected server error.",
        "download_pdf_page_title": "[admin] Your PDF files",
        "download_pdf_page_header": "Your PDF files",
        "no_pdfs": "You have no PDF files uploaded.",
        "filename": "Filename",
        "size": "Size",
        "download": "Download",
        "file_delete_success": "File deleted successfully.",
        "file_delete_error": "Error while deleting file.",
        "file_delete_not_found": "File not found.",
        "file_delete_not_selected": "File not selected.",
        "generate_fixtures": "Generate fixtures",
        "fixtures_generated": "fixtures generated.",
        "fixtures_erased": "Removed existing fixtures.",
        "show_stats": "Show stats",
        "show_stats_page_title": "[admin] Stats",
        "show_stats_page_header": "Site's stats",
        "customer_name": "Client",
        "amount": "Amount",
        "comment": "Comments",
        "stats_graph1_name": "Presence of comments",
        "stats_graph2_name": "Number of services rendered per client",
        "stats_graph3_name": "Total cost of rendered services per client",
        "logout": "Log out"
    },
}


def init_context(request):
    theme = request.session.get("theme", None)
    language = request.session.get("language", None)
    scale = request.session.get("scale", None)

    if theme is None:
        if request.user.is_authenticated:
            theme = User.objects.get(id=request.user.id).theme
        else:
            theme = 0

    if language is None:
        if request.user.is_authenticated:
            language = User.objects.get(id=request.user.id).language
        else:
            language = "ru"

    if scale is None:
        if request.user.is_authenticated:
            scale = User.objects.get(id=request.user.id).scale
        else:
            scale = 1.0

    return {"session": {"theme": theme, "language": language, "scale": scale}, "localizator": localizator[language]}


def main(request):
    return TemplateResponse(request, "main.html")


def about(request):
    return TemplateResponse(request, "about.html")


def login_view(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('menu')
            else:
                context["error"] = "Неверная почта или пароль"
    else:
        form = LoginForm()
    context["form"] = form
    return TemplateResponse(request, "login.html", context=context)


def logout_view(request):
    auth_logout(request)
    return redirect("login")


def menu(request):
    context = init_context(request)

    return TemplateResponse(request, "menu.html", context=context)


def settings(request):
    context = init_context(request)

    if request.method == "POST":
        theme = request.POST.get("theme", 0)
        language = request.POST.get("language", "ru")
        scale = request.POST.get("scale", 1.0)

        request.session["theme"] = theme
        request.session["language"] = language
        request.session["scale"] = scale

        user = User.objects.get(id=request.user.id)
        user.theme = theme
        user.language = language
        user.scale = scale
        user.save()

    context = init_context(request)

    return TemplateResponse(request, "settings.html", context=context)


def user_list(request):
    context = init_context(request)

    users = User.objects.all()
    user_list = []
    for user in users:
        user_list.append({"id": user.id, "name": user.name})

    context.update({"users": user_list})

    return TemplateResponse(request, "user_list.html", context=context)


def user_create(request):
    context = init_context(request)

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            account = form.save()  # Сохранение нового пользователя
            User.objects.create(id=account.id, account=account, name=form.cleaned_data["username"])
            return redirect('user_list')  # Перенаправление на страницу успеха
        else:
            context.update({"error": form.errors})
    form = RegisterUserForm()
    context.update({"form": form})

    return TemplateResponse(request, 'user_create.html', context=context)


def user_update(request, id):
    context = init_context(request)

    try:
        user = User.objects.get(id=id)
        if request.method == "POST":
            form = UpdateUserForm(request.POST, lang=context["session"]["language"])
            if form.is_valid():
                user.name = form.cleaned_data["name"]
                user.save()
                return redirect("user_list")
            else:
                context.update({"error": form.errors})
        form = UpdateUserForm(lang=context["session"]["language"], initial={'name': user.name})
        context.update({"form": form})
    except ObjectDoesNotExist:
        context.update({"error": f"Пользователь с id={id} не существует."})

    return TemplateResponse(request, 'user_update.html', context=context)


def user_delete(request, id):
    context = init_context(request)
    try:
        user = User.objects.get(id=id)
        if request.method == "POST":
            account = user.account
            account.delete()
            user.delete()
            return redirect("user_list")
        else:
            context.update({"id": user.id, "name": user.name})
    except ObjectDoesNotExist:
        context.update({"error": f"Пользователь с id={id} не существует."})

    return TemplateResponse(request, 'user_delete.html', context=context)


def service_list(request):
    context = init_context(request)

    services = Services.objects.all()
    service_list = []
    for service in services:
        service_list.append({"id": service.id, "title": service.title, "desc": service.desc, "price": service.price})

    context.update({"services": service_list})

    return TemplateResponse(request, "service_list.html", context=context)


def service_create(request):
    context = init_context(request)

    if request.method == 'POST':
        form = CreateServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_list')  # Перенаправление на страницу успеха
        else:
            context.update({"error": form.errors})
    form = CreateServiceForm()
    context.update({"form": form})

    return TemplateResponse(request, 'service_create.html', context=context)


def service_update(request, id):
    context = init_context(request)

    try:
        service = Services.objects.get(id=id)
        if request.method == "POST":
            form = CreateServiceForm(request.POST)
            if form.is_valid():
                service.title = form.cleaned_data["title"]
                service.desc = form.cleaned_data["desc"]
                service.price = form.cleaned_data["price"]
                service.save()
                return redirect("service_list")
            else:
                context.update({"error": form.errors})
        form = CreateServiceForm(initial={"title": service.title, "desc": service.desc, "price": service.price})
        context.update({"form": form})
    except ObjectDoesNotExist:
        context.update({"error": f"Услуга с id={id} не существует."})

    return TemplateResponse(request, 'service_update.html', context=context)


def service_delete(request, id):
    context = init_context(request)
    try:
        service = Services.objects.get(id=id)
        if request.method == "POST":
            service.delete()
            return redirect("service_list")
        else:
            context.update({"id": service.id, "title": service.title})
    except ObjectDoesNotExist:
        context.update({"error": f"Услуга с id={id} не существует."})

    return TemplateResponse(request, 'service_delete.html', context=context)


def pdf_list(request, uid):
    context = init_context(request)

    if uid != request.user.id:
        return HttpResponseForbidden()

    user_pdf_dir = os.path.join('web_django', 'prac8', 'storage', 'pdfs', str(uid))

    files = []
    if os.path.exists(user_pdf_dir):
        files = [f for f in os.listdir(user_pdf_dir) if f.endswith('.pdf')]

    context.update({"files": files})
    return TemplateResponse(request, 'pdf_list.html', context=context)


def pdf_upload(request, uid):
    context = init_context(request)

    if uid != request.user.id:
        return HttpResponseForbidden()

    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        user_pdf_dir = os.path.join('web_django', 'prac8', 'storage', 'pdfs', str(uid))

        # Проверка на тип файла
        if not pdf_file.name.endswith('.pdf'):
            context.update({"error": localizator[context["session"]["language"]]["error_only_pdf_accepted"]})
        else:
            # Проверка на существование файла с таким же именем
            if os.path.exists(os.path.join(user_pdf_dir, pdf_file.name)):
                context.update({"error": localizator[context["session"]["language"]]["error_file_already_exists"]})
            else:
                # Проверка на размер файла (максимум 5 МБ)
                max_size = 5 * 1024 * 1024  # 5 МБ в байтах
                if pdf_file.size > max_size:
                    context.update({"error": localizator[context["session"]["language"]]["error_file_too_big"]})
                else:
                    # Создаем директорию, если она не существует
                    if not os.path.exists(user_pdf_dir):
                        os.makedirs(user_pdf_dir)

                    fs = FileSystemStorage(location=user_pdf_dir)
                    filename = fs.save(pdf_file.name, pdf_file)
                    return redirect('pdf_list', uid=uid)

    return TemplateResponse(request, 'pdf_upload.html', context=context)


def pdf_delete(request, uid, fname):
    context = init_context(request)

    if uid != request.user.id:
        return HttpResponseForbidden()

    user_pdf_dir = os.path.join('web_django', 'prac8', 'storage', 'pdfs', str(uid))
    file_path = os.path.join(user_pdf_dir, fname)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return redirect("pdf_list", uid)
        except Exception:
            context.update({"error": localizator[context["session"]["language"]]["file_delete_error"]})
    else:
        context.update({"error": localizator[context["session"]["language"]]["file_not_found"]})

    return TemplateResponse(request, "pdf_delete.html", context=context)


def fixtures_generate(request):
    context = init_context(request)

    services = Services.objects.all()

    if not services.exists():
        context.update({"error": "Нет услуг для создания записей."})

    entries = Entries.objects.all()
    if entries:
        for entry in entries:
            entry.delete()
        context.update({"erased": 1})

    # Генерируем 75 случайных записей
    for _ in range(75):
        customer_name = fake.name()  # Генерация случайного имени клиента
        service = random.choice(services)  # Случайный выбор услуги
        amount = random.randint(1, 5)  # Случайная сумма от 1 до 5
        comment = None
        if random.randint(1, 100) < 20:
            comment = fake.sentence()  # Генерация случайного комментария с вероятностью 20%

        # Создаем запись в базе данных
        Entries.objects.create(
            customer_name=customer_name,
            service=service,
            amount=amount,
            comment=comment,
        )

    return TemplateResponse(request, "fixtures_generate.html", context=context)


def add_watermark(image_path, watermark_path):
    """Добавляет водяной знак к изображению."""
    original = Image.open(image_path)
    watermark = Image.open(watermark_path)

    # Позиционируем водяной знак в правом нижнем углу
    original.paste(watermark, (original.width - watermark.width, original.height - watermark.height), watermark)
    return original


def fixtures_stats(request):
    entries = Entries.objects.all()

    # Данные для круговой диаграммы
    comments_count = entries.filter(comment__isnull=False).count()
    no_comments_count = entries.filter(comment__isnull=True).count()

    # Построение круговой диаграммы
    plt.figure(figsize=(8, 8))
    plt.pie([comments_count, no_comments_count], labels=['С комментариями', 'Без комментариев'], autopct='%1.1f%%',
            startangle=90)
    plt.title('Количество записей с комментариями и без')
    pie_chart_path = '/web_django/prac8/storage/temp/graph1.png'
    plt.savefig(pie_chart_path)
    plt.close()

    # Данные для столбчатой диаграммы по полю amount
    amounts = [entry.amount for entry in entries]

    plt.figure(figsize=(10, 5))
    plt.bar(range(len(amounts)), amounts)
    plt.title('Число оказанных услуг клиенту')
    plt.xlabel('Запись')
    plt.ylabel('Количество')
    bar_chart_amount_path = '/web_django/prac8/storage/temp/graph2.png'
    plt.savefig(bar_chart_amount_path)
    plt.close()

    # Данные для столбчатой диаграммы суммы заказа (amount * service.price)
    order_sums = [entry.amount * entry.service.price for entry in entries]

    plt.figure(figsize=(10, 5))
    plt.bar(range(len(order_sums)), order_sums)
    plt.title('Сумма, оставленная каждым клиентом')
    plt.xlabel('Запись')
    plt.ylabel('Сумма заказа')
    bar_chart_order_sum_path = '/web_django/prac8/storage/temp/graph3.png'
    plt.savefig(bar_chart_order_sum_path)
    plt.close()

    # Добавление водяного знака к изображениям
    watermark_path = '/web_django/prac8/storage/assets/watermark.png'

    for image in ImageModel.objects.all():
        image.delete()

    id = 0
    for chart_path in [pie_chart_path, bar_chart_amount_path, bar_chart_order_sum_path]:
        id += 1
        watermarked_image = add_watermark(chart_path, watermark_path)
        watermarked_image.save(chart_path)

        image_instance = ImageModel(id=id)
        image_instance.image.save(os.path.basename(chart_path), open(chart_path, 'rb'))
        image_instance.save()

    context = init_context(request)

    context.update({'graph1': ImageModel.objects.get(id=1).image,
                    'graph2': ImageModel.objects.get(id=2).image,
                    'graph3': ImageModel.objects.get(id=3).image})

    entries = Entries.objects.all()
    entry_list = []

    for entry in entries:
        entry_list.append({"id": entry.id, "customer_name": entry.customer_name,
                           "service_title": entry.service.title, "amount": entry.amount,
                           "comment": entry.comment})

    context.update({"entries": entry_list})

    return TemplateResponse(request, "fixtures_stats.html", context=context)
