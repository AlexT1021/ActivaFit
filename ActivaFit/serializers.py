from rest_framework import serializers
from .models import Ejercicio, Rutina, RutinaEjercicio, ProgresoUsuario

# serializadores

class EjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercicio
        fields = '__all__'

class RutinaEjercicioSerializer(serializers.ModelSerializer):
    nombre_ejercicio = serializers.ReadOnlyField(source='ejercicio.nombre')
    video_ejercicio = serializers.ReadOnlyField(source='ejercicio.video_url')

    class Meta:
        model = RutinaEjercicio
        fields = ['ejercicio', 'nombre_ejercicio', 'video_ejercicio', 'sets', 'reps', 'orden']

class RutinaSerializer(serializers.ModelSerializer):
    ejercicios_detalles = RutinaEjercicioSerializer(source='rutinaejercicio_set', many=True, read_only=True)

    class Meta:
        model = Rutina
        fields = ['id', 'nombre', 'descripcion', 'nivel', 'objetivo', 'ejercicios_detalles', 'fecha_creado']

class ProgresoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgresoUsuario
        fields = '__all__'

