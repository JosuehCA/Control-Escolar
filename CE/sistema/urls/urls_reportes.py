from django.urls import path

from sistema.views import views_reportes

urlpatterns = [
    path("actualizarAsistencias", views_reportes.actualizarAsistencias, name="actualizar_asistencias"),
    path("reportesDisponibles", views_reportes.obtenerReportesDisponibles, name="reportes_disponibles"),
    path("generarHistogramaAsistencias", views_reportes.obtenerHistogramaAsistencias, name="generar_reporte"),
    path("generarDiagramaPastel/<str:tipo>", views_reportes.obtenerDiagramaPastel, name="generar_diagrama_pastel_calificaciones")
]
