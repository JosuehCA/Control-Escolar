from django.urls import path
from sistema.views import views_administrador



urlpatterns = [
    path('crearUsuario/', views_administrador.crearUsuario, name='crearUsuario'),
    path('listaUsuarios/', views_administrador.listarUsuarios, name='listaUsuarios'),
    path('eliminarUsuario/<int:usuarioId>/', views_administrador.eliminarUsuario, name='eliminarUsuario'),
    path('modificarUsuario/<int:usuarioId>/ <str:rol>', views_administrador.modificarUsuario, name='modificarUsuario')
]