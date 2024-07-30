from django.db import models

class Paciente(models.Model):
    cedula = models.CharField(max_length=20, primary_key=True)  
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    genero = models.CharField(max_length=10)
    direccion = models.CharField(max_length=200)
    celular = models.CharField(max_length=15)
    correo = models.EmailField()
    diagnostico = models.TextField()
    alergias = models.TextField()
    sintomas = models.TextField()
    medicacion = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
