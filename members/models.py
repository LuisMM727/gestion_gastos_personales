from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salario_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Salario Mínimo')

    def __str__(self):
        return f"Perfil de {self.user.username}"

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto')
    description = models.CharField(max_length=255, verbose_name='Descripción')
    category = models.CharField(max_length=100, verbose_name='Categoría')
    date = models.DateField(verbose_name='Fecha')
    image = models.ImageField(upload_to='expenses/', blank=True, null=True, verbose_name='Imagen')

    def __str__(self):
        return f"{self.description} - {self.amount}"
