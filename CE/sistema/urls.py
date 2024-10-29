from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("actividades", views.crear_actividad, name = "actividades"),
    path("lista_actividades", views.listar_actividades, name="lista_actividades"),
    path('crear_horario', views.crear_horario, name='crear_horario'),
    path('eliminar_actividad/<int:actividad_id>', views.eliminar_actividad, name='eliminar_actividad'),
]
