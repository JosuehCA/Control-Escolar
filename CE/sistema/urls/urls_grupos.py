from django.urls import path

from sistema.views import views_administrador

urlpatterns = [
    path("administrar", views_administrador.administrar, name="administrar"),
    path('crearGrupo/', views_administrador.crearGrupo, name='crearGrupo'),
    path('listaGrupos/', views_administrador.listar_grupos, name='listaGrupos'),
    path('eliminarGrupo/<int:grupoId>/', views_administrador.eliminarGrupo, name='eliminarGrupo'),
    path('actualizarGrupo/<int:grupoId>/', views_administrador.modificarGrupo, name='modificarGrupo'),
    path('crearUsuario/', views_administrador.crearUsuario, name='crearUsuario'),
    path('listaUsuarios/', views_administrador.listarUsuarios, name='listaUsuarios'),
    path('eliminarUsuario/<int:usuarioId>/', views_administrador.eliminarUsuario, name='eliminarUsuario'),
    path('modificarUsuario/<int:usuarioId>/ <str:rol>', views_administrador.modificarUsuario, name='modificarUsuario')
]
