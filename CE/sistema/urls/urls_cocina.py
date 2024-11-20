from django.urls import path

from sistema.views import views_cocina

urlpatterns = [
    path('opcionesMenu', views_cocina.opcionesMenu, name='opcionesMenu'),
    path('crearPlatillo', views_cocina.obtenerInformacionCreacionPlatillo, name='crearPlatillo'),
    path('crearMenuSemanal', views_cocina.obtenerInformacionCreacionMenu, name='crearMenuSemanal'),
    path('seleccionarMenuSemanal', views_cocina.seleccionarMenuSemanal, name='seleccionarMenuSemanal'),
    path('verMenuSemanal', views_cocina.verMenuSemanal, name='verMenuSemanal'),
    path('gestionarMenuSemanal/<int:menu_id>/', views_cocina.gestionarMenuSemanal, name='gestionarMenuSemanal'),
    path('eliminarMenu/<int:menu_id>/', views_cocina.eliminarMenu, name='eliminarMenu'),
    path('agregarPlatillo/<int:menu_id>/', views_cocina.obtenerInformacionAgregarPlatillo, name='agregarPlatillo'),
    path('editarPlatillo/<int:menu_id>/', views_cocina.obtenerInformacionModificarPlatillo, name='editarPlatillo'),
    path('eliminarPlatillo/<int:menu_id>/', views_cocina.obtenerInformacionEliminarPlatillo, name='eliminarPlatillo')
]
