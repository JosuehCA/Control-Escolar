from django.urls import path

from sistema.views import views_grupos

urlpatterns = [
    path("administrar", views_grupos.administrar, name="administrar"),
    path('grupos', views_grupos.administrarGrupos, name='administrarGrupos')
]
