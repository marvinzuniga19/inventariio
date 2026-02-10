# Sistema de Gestión de Inventario

Un sistema completo de gestión de inventario con arquitectura MVC, testing integrado y manejo robusto de errores.

## 📁 Estructura del Proyecto

```
inventario_py/
├── main.py                    # Punto de entrada original
├── main_improved.py           # Punto de entrada mejorado con MVC
├── inventory_model.py          # Modelo de datos (SQLite)
├── inventory_ui.py            # Interfaz de usuario (ttkbootstrap)
├── inventory_controller.py     # Controlador MVC (lógica de negocio)
├── inventory_config.py        # Gestión de configuración
├── inventory_validation.py    # Clases de validación
├── inventory_error_handler.py # Manejo centralizado de errores
├── tests/                    # Suite de tests unitarios
│   ├── run_tests.py         # Runner de tests
│   ├── test_inventory_model.py
│   ├── test_validation.py
│   └── test_config.py
├── requirements.txt          # Dependencias del proyecto
├── config.json            # Archivo de configuración (autogenerado)
└── inventory.log           # Log de la aplicación (autogenerado)
```

## 🏗️ Arquitectura MVC

### Model (inventory_model.py)
- **Responsabilidad**: Gestión de datos y persistencia
# Sistema de Gestión de Inventario

Proyecto en Python para gestionar un inventario con arquitectura MVC, tests y manejo centralizado de errores.

## Estructura principal

```
inventario_py/
├── main.py
├── main_improved.py
├── inventory_model.py
├── inventory_ui.py
├── inventory_controller.py
├── inventory_config.py
├── inventory_validation.py
├── inventory_error_handler.py
├── tests/
│   ├── run_tests.py
│   ├── test_inventory_model.py
│   ├── test_validation.py
│   └── test_config.py
├── requirements.txt
├── config.json        # (autogenerado en la primera ejecución)
└── inventory.log      # (autogenerado)
```

## Requisitos

- Python 3.10+ (la virtualenv incluida usa 3.14 en desarrollo)
- Virtual environment recomendado
- Dependencias en `requirements.txt` (incluye `ttkbootstrap`)
- Dependencia opcional: `reportlab` para generación de PDFs

Instalación rápida:

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
# Opcional: pip install reportlab
```

## Ejecución

- Ejecutar la interfaz principal (UI):

```bash
python main.py
```

- Ejecutar la versión mejorada (MVC explícito):

```bash
python main_improved.py
```

## Tests

- Ejecutar la suite de pruebas incluida:

```bash
python tests/run_tests.py
# o usando pytest
pytest -q
```

## Configuración

El archivo `config.json` se crea automáticamente con valores por defecto al arrancar la aplicación. Valores típicos:

```json
{
  "database": { "name": "inventario.db", "backup_folder": "backups" },
  "ui": { "theme": "superhero", "geometry": "700x500", "title": "Gestor de Inventario" },
  "validation": { "min_nombre_length": 2, "max_nombre_length": 100, "default_stock_minimo": 10 },
  "logging": { "level": "INFO", "file": "inventory.log" }
}
```

## Qué incluye el proyecto

- Arquitectura MVC separada en `inventory_model.py`, `inventory_controller.py` y `inventory_ui.py`.
- Validación centralizada en `inventory_validation.py`.
- Manejo de errores y logging en `inventory_error_handler.py`.
- Exportación a CSV/PDF (PDF requiere `reportlab`).
- Backup/restore de la base de datos SQLite.

## Desarrollo y calidad

- Tests unitarios y de integración en `tests/`.
- Herramientas recomendadas: `black`, `flake8`, `pytest`.

Comandos útiles:

```bash
# Formatear con Black
black .

# Ejecutar lint
flake8 .
```

## Próximos pasos sugeridos

- Añadir control de usuarios y permisos
- API REST para integración externa
- Mejoras en los reportes y exportación

---

Si quieres, puedo:

- Ejecutar la suite de tests y adjuntarte el resultado
- Añadir badges al README (CI, cobertura)
- Crear un archivo `CONTRIBUTING.md` y plantilla de issues

Dime qué prefieres que haga a continuación.