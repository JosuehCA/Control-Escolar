from django.urls import path

from sistema.views import views_reportes

urlpatterns = [
    path("actualizarAsistencias", views_reportes.actualizarAsistencias, name="actualizar_asistencias"),
    path("reportesDisponibles", views_reportes.reportesDisponibles, name="reportes_disponibles"),
    path("generarReporteAsistencia", views_reportes.generarReporteAsistencia, name="generar_reporte"),
    path("generarDiagramaPastel", views_reportes.generarDiagramaPastel, name="generar_diagrama_pastel")
]