from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# --- Opciones para Filtros (Nivel y Objetivo) ---
NIVEL_CHOICES = [
    ('PRINCIPIANTE', 'Principiante'),
    ('INTERMEDIO', 'Intermedio'),
    ('AVANZADO', 'Avanzado'),
]

OBJETIVO_CHOICES = [
    ('PERDIDA_PESO', 'Pérdida de Peso'),
    ('GANANCIA_MUSCULAR', 'Ganancia Muscular'),
    ('RESISTENCIA', 'Resistencia / Cardio'),
    ('FLEXIBILIDAD', 'Flexibilidad'),
]

class Ejercicio(models.Model):
    """
    Modelo para administrar los ejercicios individuales.
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Ejercicio")
    descipcion = models.TextField(verbose_name="Descripción")
    video_url = models.URLField(blank=True, null=True, verbose_name="Video de referencia")
    
    # Filtro opcional: Un ejercicio también puede tener un nivel de dificultad inherente
    dificultad = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='PRINCIPIANTE')

    def __str__(self):
        return self.nombre

class Rutina(models.Model):
    """
    Modelo para las rutinas. Incluye los filtros por objetivo y nivel.
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Rutina")
    descripcion = models.TextField(blank=True)
    
    # REQUISITO: Filtros por objetivo y nivel
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, verbose_name="Nivel")
    objetivo = models.CharField(max_length=20, choices=OBJETIVO_CHOICES, verbose_name="Objetivo")
    
    # Relación ManyToMany con Ejercicios a través de un modelo intermedio
    ejercicios = models.ManyToManyField(
        Ejercicio, 
        through='RutinaEjercicio',
        related_name='routines'
    )
    
    fecha_creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_nivel_display()} - {self.get_objetivo_display()})"

class RutinaEjercicio(models.Model):
    """
    Modelo intermedio para vincular Rutinas con Ejercicios.
    Aquí es donde validamos que no se repitan y agregamos detalles (series/reps).
    """
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    
    # Datos extra útiles para una app de fitness
    sets = models.PositiveIntegerField(default=3, verbose_name="Series")
    reps = models.PositiveIntegerField(default=10, verbose_name="Repeticiones")
    orden = models.PositiveIntegerField(default=1, verbose_name="Orden en la rutina")

    class Meta:
        verbose_name = "Ejercicio de Rutina"
        verbose_name_plural = "Ejercicios de la Rutina"
        ordering = ['orden']
        
        # REQUISITO CRÍTICO: Validar que una rutina no repita un ejercicio.
        # Esta restricción a nivel de base de datos impide duplicados.
        constraints = [
            models.UniqueConstraint(fields=['rutina', 'ejercicio'], name='unique_ejercicio_per_rutina')
        ]

    def __str__(self):
        return f"{self.ejercicio.nombre} en {self.rutina.nombre}"


class ProgresoUsuario(models.Model):
    """
    REQUISITO: Administrar progreso de usuarios.
    Registra cada vez que un usuario completa una rutina.
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progresos')
    rutina = models.ForeignKey(Rutina, on_delete=models.SET_NULL, null=True)

    fecha_completado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de finalización")
    duracion_minutos = models.PositiveIntegerField(verbose_name="Duración (minutos)", help_text="Tiempo que tomó completar la rutina")
    notas = models.TextField(blank=True, verbose_name="Notas del usuario", help_text="¿Cómo se sintió el usuario?")

    def __str__(self):
        return f"{self.usuario.username} - {self.rutina.nombre if self.rutina else 'Rutina eliminada'} - {self.fecha_completado.date()}"