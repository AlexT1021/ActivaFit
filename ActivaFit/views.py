from rest_framework import viewsets, permissions, filters
from .models import Ejercicio, Rutina, RutinaEjercicio, ProgresoUsuario
from .serializers import EjercicioSerializer, RutinaSerializer, RutinaEjercicioSerializer, ProgresoUsuarioSerializer


# Create your views here.

class EjercicioViewSet(viewsets.ModelViewSet):
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer
    permission_classes = [permissions.IsAuthenticated]

class RuntinaViewSet(viewsets.ModelViewSet):
    queryset = Rutina.objects.all()
    serializer_class = RutinaSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProgresoUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = ProgresoUsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProgresoUsuario.objects.filter(usuario=self.request.usuario)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.usuario)