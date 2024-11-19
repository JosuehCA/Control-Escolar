from django.urls import path

from sistema.views import views_reportes

urlpatterns = [
    path("generarReporteAsistencia", views_reportes.generarReporteAsistencia, name="generar_reporte"),
    path("generarDiagramaPastel", views_reportes.generarDiagramaPastel, name="generar_diagrama_pastel")
]