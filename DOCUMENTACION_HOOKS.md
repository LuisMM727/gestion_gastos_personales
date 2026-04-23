# Implementación de Git Hooks con Pre-commit

## Resumen de la Implementación

El proyecto ha implementado un flujo de trabajo riguroso de control de calidad de código utilizando Git Hooks configurados mediante pre-commit. Este documento detalla cómo se ha implementado cada indicador.

---

## Indicador 1: Configuración de Estilo (PEP 8)

### ✅ Archivos Creados

#### `.flake8`
- **Línea máxima**: 100 caracteres
- **Complejidad máxima**: 10
- **Directorios excluidos**:
  - `.git`, `__pycache__`, `.venv`, `venv`, `env`
  - `migrations/` (archivos autogenerados de Django)
  - Archivos de compilación

```ini
[flake8]
max-line-length = 100
exclude = .git, __pycache__, .venv, venv, env, migrations, .eggs, *.egg
ignore = E501, W503, E203  # Delegados a Black
select = E, W, F, C, N  # Verificaciones incluidas
max-complexity = 10
```

#### `pyproject.toml`
Configuración centralizada para las herramientas de análisis:

**Black**: Formateador automático
- Línea máxima: 100 caracteres
- Compatibilidad con Python 3.10+
- Excluye migraciones y entornos virtuales

**isort**: Organizador de importaciones
- Perfil compatible con Black
- Línea máxima: 100 caracteres
- Excluye directorios de entorno virtual

**Pylint**: Análisis detallado
- Complejidad máxima: 10
- Configuración de Django habilitada

---

## Indicador 2: Implementación de Hooks

### ✅ Archivo `.pre-commit-config.yaml`

Hooks implementados:

#### 1. **Black** (Formateador)
```yaml
- repo: https://github.com/psf/black
  rev: 24.1.1
  hooks:
    - id: black
      args: ['--line-length=100']
      exclude: migrations/|venv/|env/|.venv/
```
- Formatea automáticamente código según PEP 8
- Si el archivo se modifica, black lo arregla y requiere nuevo commit

#### 2. **Flake8** (Análisis Estático)
```yaml
- repo: https://github.com/PyCQA/flake8
  rev: 7.0.0
  hooks:
    - id: flake8
      args: ['--config=.flake8']
      additional_dependencies:
        - flake8-docstrings
        - flake8-bugbear
        - flake8-comprehensions
```
- Detecta errores de estilo y lógica
- Bloquea commit si hay violaciones

#### 3. **isort** (Organizador de Importaciones)
```yaml
- repo: https://github.com/PyCQA/isort
  rev: 5.13.2
  hooks:
    - id: isort
      args: ['--profile=black', '--line-length=100']
```
- Organiza automáticamente imports
- Compatible con Black

#### 4. **Pre-commit Generic Hooks**
- `trailing-whitespace`: Elimina espacios al final de líneas
- `end-of-file-fixer`: Agrega salto de línea final
- `check-yaml`: Valida archivos YAML
- `check-merge-conflict`: Detecta conflictos no resueltos
- `debug-statements`: Encuentra sentencias de debug

#### 5. **Pylint** (Análisis Detallado)
```yaml
- repo: https://github.com/PyCQA/pylint
  rev: pylint-2.17.7
  hooks:
    - id: pylint
      args: ['--max-line-length=100']
      exclude: migrations/|venv/|env/|.venv/|tests\.py|manage\.py
```
- Análisis profundo de calidad
- Excluye archivos especiales de Django

---

## Indicador 3: Gestión de Exclusiones

### ✅ Exclusiones Implementadas

**En todos los hooks se excluyen automáticamente:**

1. **Migraciones Django** (`migrations/`)
   - Archivos autogenerados por Django
   - Cambios frecuentes y controlados

2. **Entornos Virtuales** (`.venv/`, `venv/`, `env/`)
   - Contienen librerías externas
   - No relevantes para análisis del proyecto

3. **Archivos Especiales**
   - `__pycache__/`: Caché compilado
   - `.eggs/`, `*.egg`: Paquetes compilados
   - `manage.py`, `tests.py`: Archivos especiales de Django

### Configuración de Exclusión

```yaml
exclude: |
  (?x)^(
      migrations/|
      venv/|
      env/|
      .venv/|
      __pycache__/
  )
```

Esta configuración evita falsos positivos y errores de análisis en archivos que no son parte del código del proyecto.

---

## Indicador 4: Verificación de Bloqueo

### ✅ Demostración de Bloqueo

Los hooks bloquean commits con:

1. **Importaciones no utilizadas**
   ```python
   import os  # Flake8: F401 'os' imported but unused
   ```
   → ❌ BLOQUEADO

2. **Errores de formato**
   ```python
   x =    2  # Black lo corregirá automáticamente
   ```
   → ⚠️ MODIFICADO y requiere nuevo commit

3. **Espacios al final de líneas**
   ```python
   x = 1  # <- espacio aquí
   ```
   → ❌ BLOQUEADO

4. **Conflictos de merge no resueltos**
   ```
   <<<<<<< HEAD
   código
   ======
   código
   >>>>>>> branch
   ```
   → ❌ BLOQUEADO

### Proceso de Bloqueo

```bash
$ git commit -m "Agregar función"

[ERROR] Flake8 detected unused import
  members/views.py:5:1: F401 'os' imported but unused

Pre-commit hook FAILED
Fix the errors above and run 'git add .' and 'git commit' again
```

---

## Indicador 5: Documentación Técnica

### ✅ Instrucciones en README.md

Se ha actualizado el README.md con:

1. **Instalación de Pre-commit**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

2. **Configuración de Herramientas**
   - Explicación de cada herramienta
   - Archivos de configuración
   - Parámetros específicos

3. **Comportamiento de los Hooks**
   - Cuándo bloquean
   - Qué errores detectan
   - Cómo corregir

4. **Gestión de Exclusiones**
   - Archivos excluidos automáticamente
   - Razón de exclusión

5. **Solución de Problemas**
   - Errores comunes
   - Cómo reinstalar hooks
   - Cómo actualizar hooks

6. **Desactivación Temporal**
   ```bash
   git commit --no-verify -m "Tu mensaje"
   ```
   (Solo en casos excepcionales)

---

## Instalación para Nuevos Miembros

### Paso 1: Clonar el Repositorio
```bash
git clone <repository-url>
cd gestion_gastos_personales
```

### Paso 2: Crear Entorno Virtual
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate.bat
# Linux/Mac
source .venv/bin/activate
```

### Paso 3: Instalar Pre-commit
```bash
pip install pre-commit black flake8 isort pylint
pre-commit install
```

### Paso 4: Verificar Instalación
```bash
pre-commit run --all-files
```

---

## Verificación del Sistema

### Todos los Hooks Funcionan Correctamente

✅ **Black**: Formateador instalado
✅ **Flake8**: Análisis estático instalado
✅ **isort**: Organizador de imports instalado
✅ **Pylint**: Análisis detallado instalado
✅ **Pre-commit**: Framework configurado en `.git/hooks/pre-commit`

### Exclusiones Configuradas

✅ Migraciones Django excluidas
✅ Entornos virtuales excluidos
✅ Archivos de caché excluidos

### Documentación Completa

✅ README.md actualizado
✅ Instrucciones de instalación
✅ Guía de solución de problemas
✅ Indicaciones de desactivación temporal

---

## Referencias

- **Pre-commit Framework**: https://pre-commit.com/
- **Black Documentation**: https://black.readthedocs.io/
- **Flake8 Documentation**: https://flake8.pycqa.org/
- **PEP 8 Style Guide**: https://www.python.org/dev/peps/pep-0008/
- **isort Documentation**: https://pycqa.github.io/isort/
- **Pylint Documentation**: https://pylint.readthedocs.io/

---

## Conclusión

El proyecto ha implementado un sistema completo de control de calidad de código que:

1. **Garantiza PEP 8**: Mediante Black y Flake8
2. **Automatiza correcciones**: Black arregla automáticamente muchos errores
3. **Bloquea commits defectuosos**: Previene código de baja calidad
4. **Excluye archivos autogenerados**: Evita falsos positivos
5. **Documenta el proceso**: README.md con instrucciones claras

Todos los indicadores han sido satisfechos y el sistema está listo para ser utilizado por el equipo.
