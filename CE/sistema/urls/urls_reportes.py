from django.urls import path

from sistema.views import views_reportes

urlpatterns = [
    path("reportesDisponibles", views_reportes.obtenerReportesDisponibles, name="reportes_disponibles"),
    path("generarHistograma/<str:tipo_de_datos>/<str:alcance>", views_reportes.obtenerHistogramaPDF, name="generar_histograma"),
    path("generarDiagramaPastel/<str:tipo_de_datos>/<str:alcance>", views_reportes.obtenerDiagramaPastelPDF, name="generar_diagrama_pastel")
]
