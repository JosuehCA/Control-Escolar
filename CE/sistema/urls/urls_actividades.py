from django.urls import path

from sistema.views import views_actividades

urlpatterns = [
    path("actividades", views_actividades.crear_actividad, name="actividades"),
    path("lista_actividades", views_actividades.listar_actividades, name="lista_actividades"),
    path('actividades/actualizar/<int:actividad_id>/', views_actividades.actualizar_actividad, name='actualizar_actividad'),
    path('actividad/<int:id>/', views_actividades.detalle_actividad, name='detalle_actividad'),
    path('crear_horario', views_actividades.crear_horario, name='crear_horario'),
    path('lista-horarios/', views_actividades.listar_horarios, name='lista_horarios'),
    path('eliminar-horario/<int:horario_id>/', views_actividades.eliminar_horario, name='eliminar_horario'),
    path('eliminar_actividad/<int:actividad_id>', views_actividades.eliminar_actividad, name='eliminar_actividad'),
]