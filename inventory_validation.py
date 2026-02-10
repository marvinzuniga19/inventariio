"""
Input validation classes for inventory management system.
"""

import re
from typing import List, Optional, Union
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of input validation."""
    is_valid: bool
    errors: List[str]


class ProductValidator:
    """Validator for product data."""
    
    def __init__(self):
        """Initialize validator with validation rules."""
        self.min_nombre_length = 2
        self.max_nombre_length = 100
        self.min_cantidad = 0
        self.max_cantidad = 999999
        self.min_precio = 0.0
        self.max_precio = 999999.99
        self.min_stock_minimo = 0
        self.max_stock_minimo = 999999
    
    def validate_product(self, nombre: str, cantidad: Union[str, int], 
                      precio: Union[str, float], stock_minimo: Union[str, int] = 10) -> ValidationResult:
        """Validate complete product data."""
        errors = []
        
        # Validate nombre
        nombre_errors = self.validate_nombre(nombre)
        errors.extend(nombre_errors)
        
        # Validate cantidad
        cantidad_errors = self.validate_cantidad(cantidad)
        errors.extend(cantidad_errors)
        
        # Validate precio
        precio_errors = self.validate_precio(precio)
        errors.extend(precio_errors)
        
        # Validate stock_minimo
        stock_minimo_errors = self.validate_stock_minimo(stock_minimo)
        errors.extend(stock_minimo_errors)
        
        return ValidationResult(is_valid=len(errors) == 0, errors=errors)
    
    def validate_nombre(self, nombre: str) -> List[str]:
        """Validate product name."""
        errors = []
        
        if not nombre or not str(nombre).strip():
            errors.append("El nombre del producto es obligatorio")
            return errors
        
        nombre = str(nombre).strip()
        
        if len(nombre) < self.min_nombre_length:
            errors.append(f"El nombre debe tener al menos {self.min_nombre_length} caracteres")
        
        if len(nombre) > self.max_nombre_length:
            errors.append(f"El nombre no puede exceder {self.max_nombre_length} caracteres")
        
        # Check for invalid characters
        if not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\-_\.]+$', nombre):
            errors.append("El nombre solo puede contener letras, números, espacios y caracteres básicos")
        
        return errors
    
    def validate_cantidad(self, cantidad: Union[str, int]) -> List[str]:
        """Validate product quantity."""
        errors = []
        
        if not cantidad:
            errors.append("La cantidad es obligatoria")
            return errors
        
        try:
            cantidad_int = int(cantidad)
            
            if cantidad_int < self.min_cantidad:
                errors.append(f"La cantidad debe ser mayor o igual a {self.min_cantidad}")
            
            if cantidad_int > self.max_cantidad:
                errors.append(f"La cantidad no puede exceder {self.max_cantidad}")
                
        except ValueError:
            errors.append("La cantidad debe ser un número entero")
        
        return errors
    
    def validate_precio(self, precio: Union[str, float]) -> List[str]:
        """Validate product price."""
        errors = []
        
        if not precio:
            errors.append("El precio es obligatorio")
            return errors
        
        try:
            precio_float = float(precio)
            
            if precio_float < self.min_precio:
                errors.append(f"El precio debe ser mayor o igual a {self.min_precio}")
            
            if precio_float > self.max_precio:
                errors.append(f"El precio no puede exceder {self.max_precio}")
                
        except ValueError:
            errors.append("El precio debe ser un número decimal")
        
        return errors
    
    def validate_stock_minimo(self, stock_minimo: Union[str, int]) -> List[str]:
        """Validate minimum stock."""
        errors = []
        
        if not stock_minimo:
            return errors  # stock_minimo is optional, use default
        
        try:
            stock_int = int(stock_minimo)
            
            if stock_int < self.min_stock_minimo:
                errors.append(f"El stock mínimo debe ser mayor o igual a {self.min_stock_minimo}")
            
            if stock_int > self.max_stock_minimo:
                errors.append(f"El stock mínimo no puede exceder {self.max_stock_minimo}")
                
        except ValueError:
            errors.append("El stock mínimo debe ser un número entero")
        
        return errors


class DatabaseValidator:
    """Validator for database operations."""
    
    @staticmethod
    def validate_producto_id(producto_id: Union[str, int]) -> ValidationResult:
        """Validate product ID."""
        errors = []
        
        if not producto_id:
            errors.append("El ID del producto es obligatorio")
            return ValidationResult(is_valid=False, errors=errors)
        
        try:
            id_int = int(producto_id)
            
            if id_int <= 0:
                errors.append("El ID del producto debe ser mayor que cero")
            
        except ValueError:
            errors.append("El ID del producto debe ser un número entero")
        
        return ValidationResult(is_valid=len(errors) == 0, errors=errors)
    
    @staticmethod
    def validate_filename(filename: str) -> ValidationResult:
        """Validate file name for backup/restore operations."""
        errors = []
        
        if not filename or not str(filename).strip():
            errors.append("El nombre del archivo es obligatorio")
            return ValidationResult(is_valid=False, errors=errors)
        
        filename = str(filename).strip()
        
        # Check for invalid characters
        if not re.match(r'^[a-zA-Z0-9_\-\.\\/]+$', filename):
            errors.append("El nombre del archivo contiene caracteres inválidos")
        
        return ValidationResult(is_valid=len(errors) == 0, errors=errors)


class FilterValidator:
    """Validator for search filters."""
    
    @staticmethod
    def validate_search_filter(filtro: str) -> ValidationResult:
        """Validate search filter."""
        errors = []
        
        if not filtro:
            return ValidationResult(is_valid=True, errors=errors)
        
        filtro = str(filtro).strip()
        
        if len(filtro) > 100:
            errors.append("El filtro de búsqueda es demasiado largo")
        
        return ValidationResult(is_valid=len(errors) == 0, errors=errors)