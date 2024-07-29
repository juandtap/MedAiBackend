from django.db import models

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    id_paciente = models.CharField(max_length=50, unique=True)  # Usamos 'id_paciente' para evitar conflicto con el campo 'id' por defecto
    edad = models.IntegerField()
    genero = models.CharField(max_length=10)
    direccion = models.CharField(max_length=255)
    celular = models.CharField(max_length=15)
    correo = models.EmailField()
    diagnostico = models.TextField()
    alergias = models.TextField()

    def __str__(self):
        return self.nombre
