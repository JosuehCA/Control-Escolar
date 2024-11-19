from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("administrar", views.administrar, name="administrar"),
    path('grupos', views.administrarGrupos, name='administrarGrupos'),
    path('opcionesMenu', views.opcionesMenu, name='opcionesMenu'),
    path('crearPlatillo', views.crearPlatillo, name='crearPlatillo'),
    path('crearMenuSemanal', views.crearMenuSemanal, name='crearMenuSemanal'),
    path('seleccionarMenuSemanal', views.seleccionarMenuSemanal, name='seleccionarMenuSemanal'),
    path('verMenuSemanal', views.verMenuSemanal, name='verMenuSemanal'),
    path('gestionarMenuSemanal/<int:menu_id>/', views.gestionarMenuSemanal, name='gestionarMenuSemanal'),
    path('eliminarMenu/<int:menu_id>/', views.eliminarMenu, name='eliminarMenu'),
    path('agregarPlatillo/<int:menu_id>/', views.agregarPlatillo, name='agregarPlatillo'),
    path('editarPlatillo/<int:menu_id>/', views.editarPlatillo, name='editarPlatillo'),
    path('eliminarPlatillo/<int:menu_id>/', views.eliminarPlatillo, name='eliminarPlatillo')
]
