from django.db import models
from django.contrib.auth.models import User
import datetime

# ==========================================
# TABLA UserProfile
# ==========================================


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salario_minimo = models.DecimalField(
        max_digits=12, decimal_places=0, default=0, verbose_name="Salario Mínimo"
    )

    def __str__(self):
        return f"Perfil de {self.user.username}"


# ==========================================
# TABLA Expense
# ==========================================


class Expense(models.Model):
    CATEGORIAS_CHOICES = [
        ("alimentacion", "Alimentación"),
        ("educacion", "Educación"),
        ("ocio", "Ocio"),
        ("salud", "Salud"),
        ("servicios", "Servicios Públicos"),
        ("transporte", "Transporte"),
        ("otros", "Otros"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Monto")
    description = models.CharField(max_length=255, verbose_name="Descripción")
    category = models.CharField(
        max_length=100,
        choices=CATEGORIAS_CHOICES,
        default="otros",
        verbose_name="Categoría",
    )
    date = models.DateField(default=datetime.date.today, verbose_name="Fecha")
    image = models.ImageField(
        upload_to="expenses/", blank=True, null=True, verbose_name="Imagen"
    )

    def __str__(self):
        return f"{self.description} - {self.amount}"
