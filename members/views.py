from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expense, UserProfile
from .forms import ExpenseForm, UserRegisterForm, UserProfileForm
import datetime
from django.core.paginator import Paginator

# ==========================================
# BLOQUE 1: GESTIÓN DE USUARIOS Y PERFIL
# ==========================================


# Maneja el registro de nuevos usuarios
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Cuenta creada exitosamente. Ahora puedes iniciar sesión."
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "members/register.html", {"form": form})


# Gestiona el perfil del usuario autenticado
@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado exitosamente.")
            return redirect("expense_list")
    else:
        form = UserProfileForm(instance=profile)
    return render(request, "members/profile.html", {"form": form})


# Página de inicio: redirige si ya estás logueado o muestra el registro
def home(request):
    if request.user.is_authenticated:
        return redirect("expense_list")
    # Si no está autenticado, mostrar el formulario de registro directamente
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Cuenta creada exitosamente. Ahora puedes iniciar sesión."
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "members/register.html", {"form": form})


# ==========================================
# BLOQUE 2: CRUD DE GASTOS (Leer, Crear, Editar, Borrar)
# ==========================================


# LISTAR: Muestra todos los gastos del usuario y hace cálculos financieros
@login_required
def expense_list(request):
    # 1. Obtenemos todos los gastos del usuario ordenados por fecha descendente
    expenses_list = Expense.objects.filter(user=request.user).order_by("-date")

    # 2. Lógica financiera (se mantiene igual)
    total_gastado = sum(expense.amount for expense in expenses_list)
    profile = UserProfile.objects.filter(user=request.user).first()
    salario_minimo = profile.salario_minimo if profile else 0
    diferencia = salario_minimo - total_gastado if salario_minimo > 0 else 0

    # 3. Configuración del Paginador (Ejemplo: 6 gastos por página)
    paginator = Paginator(expenses_list, 7)
    page_number = request.GET.get("page")  # Captura el número de página de la URL
    page_obj = paginator.get_page(
        page_number
    )  # Obtiene los registros de esa página específica

    return render(
        request,
        "members/expense_list.html",
        {
            "expenses": page_obj,  # IMPORTANTE: Ahora enviamos el objeto de página
            "total_gastado": total_gastado,
            "salario_minimo": salario_minimo,
            "diferencia": diferencia,
        },
    )


# CREAR: Procesa el formulario para añadir un nuevo gasto


@login_required
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, "Gasto creado exitosamente.")
            return redirect("expense_list")
    else:
        form = ExpenseForm(initial={"date": datetime.date.today()})
    return render(request, "members/expense_form.html", {"form": form})


# ACTUALIZAR: Busca un gasto específico por su ID (pk) y lo edita


@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        form = ExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Gasto actualizado exitosamente.")
            return redirect("expense_list")
    else:
        form = ExpenseForm(instance=expense)
    return render(request, "members/expense_form.html", {"form": form})


# ELIMINAR: Borra un registro tras confirmación


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        expense.delete()
        messages.success(request, "Gasto eliminado exitosamente.")
        return redirect("expense_list")
    return render(request, "members/expense_confirm_delete.html", {"expense": expense})


# ==========================================
# BLOQUE 3: EXPORTACIÓN DE DATOS
# ==========================================


@login_required
def expense_export_excel(request):
    from openpyxl import Workbook
    from django.http import HttpResponse

    expenses = Expense.objects.filter(user=request.user)

    wb = Workbook()
    ws = wb.active
    ws.title = "Gastos"

    # Define los encabezados de las columnas en el Excel
    ws["A1"] = "Fecha"
    ws["B1"] = "Descripción"
    ws["C1"] = "Categoría"
    ws["D1"] = "Monto (Gs)"

    # Recorre los gastos de la DB y los escribe en filas del Excel
    for i, expense in enumerate(expenses, start=2):
        ws[f"A{i}"] = expense.date.strftime("%Y-%m-%d")
        ws[f"B{i}"] = expense.description
        ws[f"C{i}"] = expense.category
        ws[f"D{i}"] = float(expense.amount)

    # Configura la respuesta del navegador para que entienda que es un archivo .xlsx

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=gastos.xlsx"
    wb.save(response)
    return response
