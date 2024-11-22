from django.urls import path
from sistema.views.views_actividades import *
from sistema.views import views_actividades
from sistema.views import views_administrador



urlpatterns = [
    path("administrar", views_administrador.administrar, name="administrar"),
    path('crearGrupo/', views_administrador.crearGrupo, name='crearGrupo'),
    path('listaGrupos/', views_administrador.listar_grupos, name='listaGrupos'),
    path('eliminarGrupo/<int:grupoId>/', views_administrador.eliminarGrupo, name='eliminarGrupo'),
    path('actualizarGrupo/<int:grupoId>/', views_administrador.modificarGrupo, name='modificarGrupo'),
    path('paseDeLista/<int:grupoId>/', views_actividades.paseDeLista, name='paseDeLista'),
    path('registroDeAsistencia/<int:grupoId>/', views_actividades.registroDeAsistencia, name='registroDeAsistencia'),
    path('asignarCalificaciones/<int:grupoId>/', views_actividades.asignacionCalificaciones, name='asignarCalificaciones')
]
