from django.urls import path

from sistema.views import views_administrador

urlpatterns = [
    path("administrar", views_administrador.administrar, name="administrar"),
    path('crearGrupo/', views_administrador.crearGrupo, name='crearGrupo'),
    path('listaGrupos/', views_administrador.listar_grupos, name='listaGrupos'),
    path('eliminarGrupo/', views_administrador.eliminarGrupo, name='eliminarGrupo'),
    path('modificarGrupo', views_administrador.modificarGrupo, name='modificarGrupo'),
    path('crearUsuario/', views_administrador.crearUsuario, name='crearUsuario'),
    path('listaUsuarios/', views_administrador.listarUsuarios, name='listaUsuarios'),
    path('eliminarUsuario/', views_administrador.eliminarUsuario, name='eliminarUsuario'),
    path('modificarUsuario', views_administrador.modificarUsuario, name='modificarUsuario')
]
