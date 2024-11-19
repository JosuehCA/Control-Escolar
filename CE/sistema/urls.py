from django.urls import path

from . import views

urlpatterns = [
    path("", views.indice, name="indice"),
    path("iniciarSesion", views.iniciarSesion, name="iniciar_sesion"),
    path("cerrarSesion", views.cerrarSesion, name="cerrar_sesion"),
    path("registrarse", views.registrarse, name="registrarse"),
    path("mensajeria", views.enviarMensajeDirecto, name="mensaje_directo"),
    path("generarReporteAsistencia", views.generarReporteAsistencia, name="generar_reporte"),
    path("generarDiagramaPastel", views.generarDiagramaPastel, name="generar_diagrama_pastel"),
    path("administrar", views.administrar, name="administrar"),
    path('grupos', views.administrarGrupos, name='administrarGrupos'),
    path('opcionesMenu', views.opcionesMenu, name='opcionesMenu'),
    path('crearPlatillo', views.crearPlatillo, name='crearPlatillo'),
    path('crearMenuSemanal', views.crearMenuSemanal, name='crearMenuSemanal'),
    path('seleccionarMenuSemanal', views.seleccionarMenuSemanal, name='seleccionarMenuSemanal'),
    path('verMenuSemanal', views.verMenuSemanal, name='verMenuSemanal'),
    path('gestionarMenuSemanal/<int:menu_id>/', views.gestionarMenuSemanal, name='gestionarMenuSemanal'),
    path('eliminarMenu/<int:menu_id>/', views.eliminarMenu, name='eliminarMenu'),
    path('agregarPlatillo/<int:menu_id>/', views.agregarPlatillo, name='agregarPlatillo'),
    path('editarPlatillo/<int:menu_id>/', views.editarPlatillo, name='editarPlatillo'),
    path('eliminarPlatillo/<int:menu_id>/', views.eliminarPlatillo, name='eliminarPlatillo')
]
