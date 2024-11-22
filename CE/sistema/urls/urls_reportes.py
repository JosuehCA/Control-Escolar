from django.urls import path

from sistema.views import views_reportes

urlpatterns = [
    path("actualizarAsistencias", views_reportes.actualizarAsistencias, name="actualizar_asistencias"),
    path("reportesDisponibles", views_reportes.obtenerReportesDisponibles, name="reportes_disponibles"),
    path("generarHistograma/<str:tipo_de_datos>/<str:alcance>", views_reportes.obtenerHistograma, name="generar_reporte"),
    path("generarDiagramaPastel/<str:tipo_de_datos>/<str:alcance>", views_reportes.obtenerDiagramaPastel, name="generar_diagrama_pastel_calificaciones")
]
