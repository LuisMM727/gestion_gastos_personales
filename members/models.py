# models.py
# Este archivo define los modelos de datos para la aplicación de gestión de gastos.

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# ==========================================================
# TABLA 1: UserProfile (Extensión de datos del usuario)
# ==========================================================


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    salario_minimo = models.DecimalField(
        max_digits=12, decimal_places=0, default=0, verbose_name="Salario Mínimo"
    )

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"

    def __str__(self):
        return f"Perfil de {self.user.username}"


# ==========================================================
# TABLA 2: Expense (Registro de los gastos diarios)
# ==========================================================


class Expense(models.Model):
    # Opciones de categoría predefinidas para los gastos
    # Estas categorías ayudan a organizar los gastos y facilitan el análisis posterior.
    class Category(models.TextChoices):
        ALIMENTACION = "alimentacion", "Alimentación"
        EDUCACION = "educacion", "Educación"
        OCIO = "ocio", "Ocio"
        SALUD = "salud", "Salud"
        SERVICIOS = "servicios", "Servicios Públicos"
        TRANSPORTE = "transporte", "Transporte"
        OTROS = "otros", "Otros"

    # Cada gasto está vinculado a un usuario específico
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Monto")
    description = models.CharField(max_length=255, verbose_name="Descripción")
    category = models.CharField(
        max_length=100,
        choices=Category.choices,
        default=Category.OTROS,
        verbose_name="Categoría",
    )

    date = models.DateField(default=timezone.now, verbose_name="Fecha")
    image = models.ImageField(
        upload_to="expenses/%Y/%m/",  # Organiza fotos por año/mes automáticamente
        blank=True,
        null=True,
        verbose_name="Imagen",
    )

    # Metadatos para el modelo Expense que definen cómo se muestra en el admin y el orden de los registros
    class Meta:
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"
        ordering = [
            "-date"
        ]  # Ordena los gastos por fecha, mostrando los más recientes primero

    def __str__(self):
        return f"{self.description} ({self.get_category_display()}) - {self.amount}"
