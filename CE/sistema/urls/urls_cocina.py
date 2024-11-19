from django.urls import path

from sistema.views import views_cocina

urlpatterns = [
    path('opcionesMenu', views_cocina.opcionesMenu, name='opcionesMenu'),
    path('crearPlatillo', views_cocina.crearPlatillo, name='crearPlatillo'),
    path('crearMenuSemanal', views_cocina.crearMenuSemanal, name='crearMenuSemanal'),
    path('seleccionarMenuSemanal', views_cocina.seleccionarMenuSemanal, name='seleccionarMenuSemanal'),
    path('verMenuSemanal', views_cocina.verMenuSemanal, name='verMenuSemanal'),
    path('gestionarMenuSemanal/<int:menu_id>/', views_cocina.gestionarMenuSemanal, name='gestionarMenuSemanal'),
    path('eliminarMenu/<int:menu_id>/', views_cocina.eliminarMenu, name='eliminarMenu'),
    path('agregarPlatillo/<int:menu_id>/', views_cocina.agregarPlatillo, name='agregarPlatillo'),
    path('editarPlatillo/<int:menu_id>/', views_cocina.editarPlatillo, name='editarPlatillo'),
    path('eliminarPlatillo/<int:menu_id>/', views_cocina.editarPlatillo, name='eliminarPlatillo')
]
