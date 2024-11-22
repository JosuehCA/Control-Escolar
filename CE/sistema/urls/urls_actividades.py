from django.urls import path

from sistema.views import views_actividades

urlpatterns = [
    path('crearActividad/', views_actividades.creacionActividad, name='crearActividad'),
    path('listaActividades/', views_actividades.listaActividades, name='listaActividades'),
    path('actualizar/<int:actividadId>/', views_actividades.actualizacionActividad, name='actualizarActividad'),
    path('detallesActividad/<int:actividadId>/', views_actividades.detallesDeActividad, name='detallesDeActividad'),
    path('crearHorario/', views_actividades.creacionHorario, name='crearHorario'),
    path('listaHorarios/', views_actividades.listaHorarios, name='listaHorarios'),
    path('eliminarHorario/<int:horarioId>/', views_actividades.eliminacionHorario, name='eliminarHorario'),
    path('eliminarActividad/<int:actividadId>', views_actividades.eliminacionActividad, name='eliminarActividad'),
]