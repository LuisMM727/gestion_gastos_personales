Descripción
Este sistema es una aplicación web diseñada para el control financiero individual. Permite a los usuarios registrar ingresos y egresos, categorizar sus movimientos, y visualizar el balance total en tiempo real. Construido bajo una arquitectura robusta, facilita la persistencia de datos y ofrece una interfaz administrativa para la gestión de usuarios y categorías.

Clonar el repositorio
Abre tu terminal y ejecuta el siguiente comando para descargar el código:
git clone https://github.com/tu-usuario/nombre-del-repo.git
cd nombre-del-repo

Inicializar Entorno Virtual:

python -m venv myworld

Encender Entorno Virtual:
myworld\Scripts\activate.bat

## Configuración de Calidad de Código (Pre-commit Hooks)

Este proyecto implementa un flujo de trabajo riguroso de validación de código usando Git Hooks. Esto garantiza que solo código que cumple con los estándares PEP 8 y análisis estático pase a ser commiteado.

### Herramientas Utilizadas:
- **Black**: Formateador de código automático siguiendo PEP 8
- **Flake8**: Análisis estático para detectar errores y problemas de estilo
- **isort**: Organizador automático de importaciones
- **Pylint**: Análisis detallado de calidad del código
- **pre-commit**: Framework para gestionar Git Hooks

### Instalación de Pre-commit (Obligatorio)

#### 1. Instalar pre-commit en el entorno virtual:
```bash
pip install pre-commit
```

#### 2. Instalar los Git Hooks en el repositorio:
```bash
pre-commit install
```

Este comando configura automáticamente los hooks en `.git/hooks/` para ejecutarse antes de cada commit.

#### 3. Ejecutar los hooks manualmente (opcional):
```bash
# Verificar todos los archivos
pre-commit run --all-files

# Verificar solo archivos modificados
pre-commit run
```

### Configuraciones de Estilo

#### .flake8
Define las reglas de análisis estático:
- Línea máxima: 100 caracteres
- Excluye automáticamente: migraciones, .venv, y archivos autogenerados
- Complejidad máxima: 10

#### pyproject.toml
Configuración de Black e isort:
- Línea máxima: 100 caracteres
- Perfil de isort compatible con Black
- Excluye directorios de entorno virtual y migraciones

#### .pre-commit-config.yaml
Define los hooks que se ejecutarán:
- Formateador automático (Black)
- Análisis estático (Flake8)
- Organizador de importaciones (isort)
- Validación de espacios en blanco
- Detección de conflictos de merge

### Comportamiento de los Hooks

**Los hooks BLOQUEARÁN el commit si detectan:**
- Importaciones no utilizadas
- Errores de formato de código
- Violaciones de PEP 8
- Líneas con espacios en blanco al final
- Archivos sin salto de línea final
- Conflictos de merge no resueltos

**Ejemplo de bloqueo:**
```bash
$ git commit -m "Agregar nueva función"

[ERROR] Flake8 detected unused import
  members/views.py:5:1: F401 'os' imported but unused

Pre-commit hook FAILED. Arregla los errores y intenta de nuevo.
```

### Cómo Corregir Errores

1. **Black arreglará automáticamente** muchos errores de formato
2. **isort reorganizará importaciones** automáticamente
3. **Errores de Flake8** debes corregirlos manualmente

Después de hacer correcciones, intenta el commit nuevamente.

### Gestión de Exclusiones

El proyecto excluye automáticamente:
- `migrations/`: Archivos autogenerados por Django
- `.venv/`, `venv/`, `env/`: Entornos virtuales
- `__pycache__/`: Archivos de caché de Python
- `tests.py`, `manage.py`: Archivos especiales

Esto evita falsos positivos en archivos autogenerados.

### Desactivar Temporalmente los Hooks (No Recomendado)

Si necesitas hacer skip de los hooks en un commit específico:
```bash
git commit --no-verify -m "Tu mensaje"
```

**ADVERTENCIA**: Esto saltará todas las validaciones. Solo úsalo en casos excepcionales.

### Solución de Problemas

#### Error: "pre-commit not found"
```bash
pip install pre-commit
pre-commit install
```

#### Los hooks no se ejecutan
```bash
# Reinstalar los hooks
pre-commit install
```

#### Necesitas actualizar las versiones de los hooks
```bash
# Actualizar todos los hooks a las últimas versiones
pre-commit autoupdate
```

### Verificación del Setup

Para asegurar que todo está configurado correctamente:
```bash
# Ejecutar todos los hooks en todos los archivos
pre-commit run --all-files

# Deberías ver algo como:
# black....................................................................Passed
# flake8...................................................................Passed
# isort....................................................................Passed
# trailing-whitespace.....................................................Passed
# end-of-file-fixer.......................................................Passed
# check-yaml...............................................................Passed
```

### Referencias
- [Documentación oficial de pre-commit](https://pre-commit.com/)
- [Black - Python Code Formatter](https://black.readthedocs.io/)
- [Flake8 - Style Guide Enforcement](https://flake8.pycqa.org/)
- [PEP 8 - Python Enhancement Proposal](https://www.python.org/dev/peps/pep-0008/)
