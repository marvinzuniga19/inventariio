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
- **Funcionalidades**: CRUD de productos, estadísticas, backup/restore
- **Base de datos**: SQLite con migración automática

### View (inventory_ui.py)
- **Responsabilidad**: Interfaz de usuario y presentación
- **Tecnología**: ttkbootstrap (temas modernos)
- **Características**: Tooltips, atajos, menú contextual

### Controller (inventory_controller.py)
- **Responsabilidad**: Coordinación entre Model y View
- **Funcionalidades**: Lógica de negocio, validación, manejo de errores

## 🔧 Componentes de Calidad

### Configuración (inventory_config.py)
- **Formato**: JSON con valores por defecto
- **Secciones**: Database, UI, Validation, Logging, Export, Alerts
- **Características**: Validación, recarga dinámica

### Validación (inventory_validation.py)
- **Clases**: ProductValidator, DatabaseValidator, FilterValidator
- **Características**: Reglas configurables, errores específicos
- **Tipado**: Resultados estructurados con dataclasses

### Manejo de Errores (inventory_error_handler.py)
- **Jerarquía**: Clases específicas de excepciones
- **Centralización**: ErrorHandler con callbacks registrables
- **Decoradores**: @safe_execute y @validate_and_execute

## 🧪 Testing

### Suite de Tests
- **36 tests**: Cubren modelo, validación y configuración
- **Cobertura**: CRUD, estadísticas, backup/restore, validación
- **Ejecución**: `python tests/run_tests.py`

### Tipos de Tests
- **Unit Tests**: Lógica de negocio y validación
- **Integration Tests**: Operaciones de base de datos
- **Configuration Tests**: Gestión de configuración

## 🚀 Instalación y Uso

### Instalación
```bash
# Clonar o descargar el proyecto
cd inventario_py

# Instalar dependencias
pip install -r requirements.txt

# Para funcionalidad PDF (opcional)
pip install reportlab
```

### Ejecución
```bash
# Versión original
python main.py

# Versión mejorada con MVC
python main_improved.py
```

### Testing
```bash
# Ejecutar todos los tests
python tests/run_tests.py

# Ejecutar tests específicos
python -m unittest tests.test_inventory_model -v
```

## 📋 Características Implementadas

### 🎯 Funcionalidad Básica
- ✅ CRUD completo de productos
- ✅ Validación de datos
- ✅ Búsqueda y filtrado
- ✅ Exportación CSV y PDF

### 🎨 Experiencia de Usuario
- ✅ Atajos de teclado
- ✅ Indicadores visuales de stock
- ✅ Menú contextual (click derecho)
- ✅ Tooltips e iconos

### 📊 Datos y Reportes
- ✅ Estadísticas en tiempo real
- ✅ Sistema de alertas
- ✅ Reportes PDF profesionales
- ✅ Backup/Restore de base de datos

### 🏗️ Calidad y Arquitectura
- ✅ Arquitectura MVC limpia
- ✅ Testing unitario completo
- ✅ Configuración externa
- ✅ Manejo robusto de errores

## 🔀 Flujo de Datos

```
Usuario → UI → Controller → Model → Database
         ↓      ↓          ↓        ↓
     Validar → Validar → Validar → SQL
         ↓      ↓          ↓        ↓
   Mostrar ← Resultado ← Error ← Resultado
```

## 📝 Configuración

El archivo `config.json` se crea automáticamente con valores por defecto:

```json
{
  "database": {
    "name": "inventario.db",
    "backup_folder": "backups"
  },
  "ui": {
    "theme": "superhero",
    "geometry": "700x500",
    "title": "Gestor de Inventario"
  },
  "validation": {
    "min_nombre_length": 2,
    "max_nombre_length": 100,
    "default_stock_minimo": 10
  },
  "logging": {
    "level": "INFO",
    "file": "inventory.log"
  }
}
```

## 🐛 Manejo de Errores

- **Logging**: Todos los errores se registran en `inventory.log`
- **Excepciones**: Jerarquía de excepciones específicas
- **Callbacks**: Manejo específico por tipo de error
- **Recuperación**: Sistema intenta recuperarse de errores

## 📈 Métricas de Calidad

- **Tests**: 36 tests unitarios pasando
- **Cobertura**: Funcionalidad principal cubierta
- **Arquitectura**: Separación MVC clara
- **Errores**: Manejo centralizado y logging
- **Configuración**: Externa y validada

## 🔄 Próximos Pasos

El sistema está listo para producción con:
- **Arquitectura escalable**
- **Testing completo**
- **Manejo de errores robusto**
- **Configuración flexible**

Considerar futuras mejoras:
- Multi-usuario y permisos
- Importación masiva
- API REST
- Reportes avanzados