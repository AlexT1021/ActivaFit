from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Ejercicio, Rutina, RutinaEjercicio, ProgresoUsuario
from .serializers import EjercicioSerializer, RutinaSerializer, RutinaEjercicioSerializer, ProgresoUsuarioSerializer


# Create your views here.

class EjercicioViewSet(viewsets.ModelViewSet):
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer
    permission_classes = [permissions.IsAuthenticated]

class RutinaViewSet(viewsets.ModelViewSet):
    queryset = Rutina.objects.all()
    serializer_class = RutinaSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProgresoUsuarioViewSet(viewsets.ModelViewSet):
    queryset = ProgresoUsuario.objects.all()
    serializer_class = ProgresoUsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProgresoUsuario.objects.filter(usuario=self.request.usuario)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

@api_view(['POST'])
def registrar_view(request):
    usuario = request.data.get('nombre')
    contrasena = request.data.get('contrasena')
    email = request.data.get('email')

    if not usuario or not contrasena:
        return Response({"error": "Faltan datos"}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=usuario).exists():
        return Response({"error": "El usuario ya existe"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=usuario, password=contrasena, email=email)
    return Response({"mensaje": "Usuario creado exitosamente"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_view(request):
    usuario = request.data.get('nombre')
    contrasena = request.data.get('contrasena')
    user = authenticate(request, username=usuario, password=contrasena)
    
    if user is not None:
        login(request, user)
        return Response({"mensaje": "Login exitoso"})
    else:
        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"mensaje": "Logout exitoso"})
    