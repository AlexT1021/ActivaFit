from django.urls import path, include
from rest_framework import routers
from ActivaFit import views

router = routers.DefaultRouter()

router.register(r'ejercicios', views.EjercicioViewSet)
router.register(r'rutinas', views.RuntinaViewSet)
router.register(r'usuarios', views.ProgresoUsuario)

urlpatterns = [
    path('', include(router.urls))
]