from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # Página de inicio
    path("register/", views.register, name="register"),  # Registro de nuevos usuarios
    path("profile/", views.profile, name="profile"),  # Edición del perfil del usuario
    path("expenses/", views.expense_list, name="expense_list"),  # Listado de gastos
    # Las siguientes rutas manejan la creación, edición y eliminación de gastos + exportación a Excel
    path("expenses/create/", views.expense_create, name="expense_create"),
    path("expenses/<int:pk>/update/", views.expense_update, name="expense_update"),
    path("expenses/<int:pk>/delete/", views.expense_delete, name="expense_delete"),
    path("expenses/export/", views.expense_export_excel, name="expense_export_excel"),
]
