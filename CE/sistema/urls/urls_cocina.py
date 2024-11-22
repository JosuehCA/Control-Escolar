from django.urls import path

from sistema.views import views_cocina

urlpatterns = [
    path('opcionesMenu', views_cocina.opcionesMenu, name='opcionesMenu'),
    path('gestionarRecomendaciones', views_cocina.gestionarRecomendaciones, name='gestionarRecomendaciones'),
    path('crearRecomendacion', views_cocina.crearRecomendacion, name='crearRecomendacion'),
    path('editarRecomendacion/<int:platillo_id>/', views_cocina.editarRecomendacion, name='editarRecomendacion'),
    path('eliminarRecomendacion/<int:platillo_id>/', views_cocina.eliminarRecomendacion, name='eliminarRecomendacion'),
    path('crearMenuSemanal', views_cocina.crearMenu, name='crearMenuSemanal'),
    path('seleccionarMenuSemanal', views_cocina.seleccionarMenuSemanal, name='seleccionarMenuSemanal'),
    path('verMenuSemanal', views_cocina.vizualizarMenuSemanal, name='verMenuSemanal'),
    path('gestionarMenuSemanal/<int:menu_id>/', views_cocina.gestionarMenuSemanal, name='gestionarMenuSemanal'),
    path('eliminarMenu/<int:menu_id>/', views_cocina.eliminarMenu, name='eliminarMenu'),
    path('agregarPlatillo/<int:menu_id>/', views_cocina.agregarPlatilloDelDia, name='agregarPlatillo'),
    path('editarPlatillo/<int:menu_id>/', views_cocina.modificarPlatilloDelDia, name='editarPlatillo'),
    path('eliminarPlatillo/<int:menu_id>/', views_cocina.eliminarPlatilloDelDia, name='eliminarPlatillo')
]
