from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autenticacion/', include("sistema.urls.urls_autenticacion")),
    path('mensajeria/', include("sistema.urls.urls_mensajeria")),
    path('reportes/', include("sistema.urls.urls_reportes")),
    path('grupos/', include("sistema.urls.urls_grupos")),
    path('cocina/', include("sistema.urls.urls_cocina")),
    path('actividades/', include("sistema.urls.urls_actividades"))
]