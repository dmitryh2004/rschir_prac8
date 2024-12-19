from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from application import views

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('menu/', views.menu, name="menu"),
    path('menu/settings/', views.settings, name="settings"),
    
    path('user/list', views.user_list, name="user_list"),
    path('user/create', views.user_create, name="user_create"),
    path('user/<int:id>/update', views.user_update, name="user_update"),
    path('user/<int:id>/delete', views.user_delete, name="user_delete"),

    path('service/list', views.service_list, name="service_list"),
    path('service/create', views.service_create, name="service_create"),
    path('service/<int:id>/update', views.service_update, name="service_update"),
    path('service/<int:id>/delete', views.service_delete, name="service_delete"),

    path('pdf/<int:uid>/list', views.pdf_list, name="pdf_list"),
    path('pdf/<int:uid>/upload', views.pdf_upload, name="pdf_upload"),
    path('pdf/<int:uid>/<str:fname>/delete', views.pdf_delete, name="pdf_delete"),

    path('fixtures/generate/', views.fixtures_generate, name="fixtures_generate"),
    path('fixtures/stats/', views.fixtures_stats, name="fixtures_stats"),

    path('about/', views.about, name="about"),
    path("", views.main, name="main")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)