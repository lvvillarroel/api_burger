from django.db import models


class Burger(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.PositiveIntegerField()
    descripcion = models.CharField(max_length=500)
    imagen = models.URLField()
    ingredientes = models.ManyToManyField('Ingredient', null=True, blank=True)

    def __str__(self):
        return self.nombre


class Ingredient(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)
    path = models.URLField(null=True)

    def __str__(self):
        return self.nombre
