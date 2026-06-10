from decimal import Decimal
from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import ExpenseForm
from .models import Expense, UserProfile


class MembersModelFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="secret123")
        self.profile = UserProfile.objects.create(user=self.user, salario_minimo=Decimal("2000000"))

    def test_user_profile_str_returns_username(self):
        """
        PRUEBA 1: Valida la representación en string del modelo UserProfile.
        - Verifica que str(UserProfile) devuelva el formato correcto "Perfil de {username}".
        - Comprueba que salario_minimo sea un valor positivo.
        """
        self.assertEqual(str(self.profile), "Perfil de testuser")
        self.assertTrue(self.profile.salario_minimo > 0)

    def test_expense_str_contains_description_and_category(self):
        """
        PRUEBA 2: Valida la representación en string del modelo Expense.
        - Crea un gasto de prueba.
        - Verifica que la descripción y categoría aparezcan en str(Expense).
        """
        expense = Expense.objects.create(
            user=self.user,
            amount=Decimal("750000"),
            description="Transporte taxi",
            category=Expense.Category.TRANSPORTE,
            date=date(2025, 5, 12),
        )
        self.assertIn("Transporte taxi", str(expense))
        self.assertIn("Transporte", str(expense))

    def test_expense_form_valid_data(self):
        """
        PRUEBA 3: Valida que ExpenseForm acepta datos válidos.
        - Envía datos correctos al formulario.
        - Verifica que form.is_valid() devuelva True.
        - Comprueba que los datos limpiados (cleaned_data) contengan tipos correctos.
        - Asegura que cantidad sea Decimal, categoría y descripción sean las esperadas.
        """
        form_data = {
            "amount": "150000",
            "description": "Cena familiar",
            "category": Expense.Category.ALIMENTACION,
            "date": "2025-01-10",
        }
        form = ExpenseForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertIsInstance(form.cleaned_data["amount"], Decimal)
        self.assertEqual(form.cleaned_data["category"], Expense.Category.ALIMENTACION)
        self.assertEqual(form.cleaned_data["description"], "Cena familiar")

    def test_expense_form_invalid_data_shows_errors(self):
        """
        PRUEBA 4: Valida que ExpenseForm rechaza datos inválidos.
        - Envía datos incompletos y mal formateados al formulario.
        - Verifica que form.is_valid() devuelva False.
        - Comprueba que cada campo problemático genere un error.
        - Verifica el mensaje específico de error en el campo 'description'.
        """
        form_data = {
            "amount": "",
            "description": "",
            "category": "invalid-category",
            "date": "not-a-date",
        }
        form = ExpenseForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("amount", form.errors)
        self.assertIn("description", form.errors)
        self.assertIn("category", form.errors)
        self.assertIn("date", form.errors)
        self.assertEqual(form.errors["description"], ["Este campo es obligatorio."])


class MembersViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="viewuser", password="secret123")
        self.client.force_login(self.user)
        self.expense1 = Expense.objects.create(
            user=self.user,
            amount=Decimal("100000"),
            description="Bus público",
            category=Expense.Category.TRANSPORTE,
            date=date(2025, 4, 1),
        )
        self.expense2 = Expense.objects.create(
            user=self.user,
            amount=Decimal("200000"),
            description="Almuerzo",
            category=Expense.Category.ALIMENTACION,
            date=date(2025, 4, 3),
        )

    def test_expense_list_filters_by_category_and_calculates_total(self):
        """
        PRUEBA 5: Valida la vista expense_list con filtros.
        - Hace una petición GET a la vista con filtro de categoría TRANSPORTE.
        - Verifica que la respuesta sea exitosa (status_code 200).
        - Comprueba que la categoría seleccionada sea TRANSPORTE en el contexto.
        - Valida que el total de gastos sea 100000 (solo TRANSPORTE).
        - Asegura que en HTML aparezca "Bus público" (TRANSPORTE) pero NO "Almuerzo" (ALIMENTACION).
        """
        response = self.client.get(
            reverse("expense_list"),
            {"category": Expense.Category.TRANSPORTE},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected_category"], Expense.Category.TRANSPORTE)
        self.assertEqual(response.context["total_gastado"], Decimal("100000"))
        self.assertContains(response, "Bus público")
        self.assertNotContains(response, "Almuerzo")

    def test_export_excel_returns_attachment_filename_and_content_type(self):
        """
        PRUEBA 6: Valida la exportación a archivo Excel.
        - Hace petición GET a expense_export_excel con fechas de filtro.
        - Verifica que la respuesta sea exitosa (status_code 200).
        - Comprueba que el tipo de contenido sea Excel (.xlsx).
        - Valida que el nombre del archivo en Content-Disposition sea correcto.
        - Asegura que la respuesta tenga contenido (bytes) para descargar.
        """
        response = self.client.get(
            reverse("expense_export_excel"),
            {"start_date": "2025-04-01", "end_date": "2025-04-30"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.assertIn("gastos_filtrados_2025-04-01_a_2025-04-30.xlsx", response["Content-Disposition"])
        self.assertGreater(len(response.content), 0)

    def test_export_pdf_returns_pdf_attachment(self):
        """
        PRUEBA 7: Valida la exportación a archivo PDF.
        - Hace petición GET a expense_export_pdf con fechas de filtro.
        - Verifica que la respuesta sea exitosa (status_code 200).
        - Comprueba que el tipo de contenido sea PDF.
        - Valida que el nombre del archivo en Content-Disposition sea correcto.
        - Asegura que el contenido comience con el encabezado PDF (%PDF).
        """
        response = self.client.get(
            reverse("expense_export_pdf"),
            {"start_date": "2025-04-01", "end_date": "2025-04-30"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn("reporte_filtrado_2025-04-01_a_2025-04-30.pdf", response["Content-Disposition"])
        self.assertTrue(response.content.startswith(b"%PDF"))
