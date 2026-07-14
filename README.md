# Gestión de Gastos Personales

Aplicación web Django para registrar gastos, categorizarlos, compararlos con el salario mínimo y exportar reportes (Excel/PDF).

## Arquitectura MTV

Django usa el patrón **Modelo–Template–Vista**:

```
gestion_gastos_personales/     # Configuración del proyecto (settings, URLs raíz)
gastos/                        # App de dominio
  models.py                    # MODELO  → UserProfile, Expense
  views/                       # VISTA   → lógica HTTP
    auth.py                    #         home, registro, perfil
    expenses.py                #         CRUD y exportación
  templates/gastos/            # TEMPLATE → HTML de la app
  templates/registration/      # TEMPLATE → login / logout
  forms.py                     # Formularios (entrada hacia modelos/vistas)
  exports.py                   # Generación Excel/PDF usada por las vistas
  urls.py                      # Rutas → vistas
  static/gastos/               # CSS/estáticos
```

Flujo: **URL → Vista → Modelo/Formulario → Template → respuesta HTML**.

## Requisitos

- Python 3.12+
- MySQL (opcional; puedes usar SQLite con `DB_ENGINE=sqlite`)

## Entorno virtual (solo `.venv`)

En este proyecto hay **un único** entorno virtual: `.venv`.

```powershell
# Crear (solo la primera vez)
python -m venv .venv

# Activar
.venv\Scripts\Activate

# Si PowerShell bloquea scripts, ejecuta una sola vez:
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# Instalar dependencias
pip install -r requirements.txt
```

## Configuración

```powershell
copy .env.example .env
```

Edita `.env` con tu `SECRET_KEY` y credenciales de MySQL (o pon `DB_ENGINE=sqlite`).

Crear la base MySQL (si usas MySQL):

```powershell
python create_db.py
```

Migraciones y servidor:

```powershell
python manage.py migrate
python manage.py runserver
```

Abre http://127.0.0.1:8000/

> **Nota:** la app se renombró de `members` a `gastos`. Si tenías una base antigua, recrea la BD (`create_db.py` + `migrate`) o vuelve a migrar desde cero.
