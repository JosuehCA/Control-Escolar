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
    path('grupo/<int:grupo_id>/pase-de-lista/', PaseDeListaView.as_view(), name='pase_de_lista'),
    path('grupo/<int:grupo_id>/detalle/', GrupoDetalleView.as_view(), name='grupo_detalle'),
    path('grupo/<int:grupo_id>/asignar_calificaciones/', views_actividades.asignar_calificaciones, name='asignar_calificaciones'),

]
