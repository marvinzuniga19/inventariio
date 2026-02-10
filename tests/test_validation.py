"""
Unit tests for input validation.
"""

import unittest
from inventory_validation import ProductValidator, ValidationResult, DatabaseValidator, FilterValidator


class TestProductValidator(unittest.TestCase):
    """Test cases for ProductValidator class."""
    
    def setUp(self):
        """Set up test environment."""
        self.validator = ProductValidator()
    
    def test_valid_product(self):
        """Test validation of valid product data."""
        result = self.validator.validate_product("Valid Product", 10, 99.99, 5)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
    
    def test_empty_nombre(self):
        """Test validation of empty product name."""
        result = self.validator.validate_product("", 10, 99.99, 5)
        
        self.assertFalse(result.is_valid)
        self.assertIn("El nombre del producto es obligatorio", result.errors)
    
    def test_short_nombre(self):
        """Test validation of too short product name."""
        result = self.validator.validate_product("A", 10, 99.99, 5)
        
        self.assertFalse(result.is_valid)
        self.assertIn("El nombre debe tener al menos", result.errors[0])
    
    def test_invalid_cantidad(self):
        """Test validation of invalid quantity."""
        result = self.validator.validate_product("Valid Product", "invalid", 99.99, 5)
        
        self.assertFalse(result.is_valid)
        self.assertIn("La cantidad debe ser un número entero", result.errors)
    
    def test_negative_cantidad(self):
        """Test validation of negative quantity."""
        result = self.validator.validate_product("Valid Product", -5, 99.99, 5)
        
        self.assertFalse(result.is_valid)
        self.assertIn("La cantidad debe ser mayor o igual a", result.errors[0])
    
    def test_invalid_precio(self):
        """Test validation of invalid price."""
        result = self.validator.validate_product("Valid Product", 10, "invalid", 5)
        
        self.assertFalse(result.is_valid)
        self.assertIn("El precio debe ser un número decimal", result.errors)
    
    def test_negative_precio(self):
        """Test validation of negative price."""
        result = self.validator.validate_product("Valid Product", 10, -99.99, 5)
        
        self.assertFalse(result.is_valid)
        self.assertIn("El precio debe ser mayor o igual a", result.errors[0])
    
    def test_special_characters_in_nombre(self):
        """Test validation of special characters in product name."""
        result = self.validator.validate_product("Product@#$", 10, 99.99, 5)
        
        self.assertFalse(result.is_valid)
        self.assertIn("El nombre solo puede contener", result.errors[0])
    
    def test_valid_special_characters_in_nombre(self):
        """Test validation of allowed special characters in product name."""
        result = self.validator.validate_product("Producto-123_áéíóú", 10, 99.99, 5)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
    
    def test_optional_stock_minimo(self):
        """Test validation with optional stock minimum."""
        result = self.validator.validate_product("Valid Product", 10, 99.99, None)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)


class TestDatabaseValidator(unittest.TestCase):
    """Test cases for DatabaseValidator class."""
    
    def test_valid_producto_id(self):
        """Test validation of valid product ID."""
        result = DatabaseValidator.validate_producto_id(123)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
    
    def test_invalid_producto_id(self):
        """Test validation of invalid product ID."""
        result = DatabaseValidator.validate_producto_id("invalid")
        
        self.assertFalse(result.is_valid)
        self.assertIn("El ID del producto debe ser un número entero", result.errors)
    
    def test_negative_producto_id(self):
        """Test validation of negative product ID."""
        result = DatabaseValidator.validate_producto_id(-1)
        
        self.assertFalse(result.is_valid)
        self.assertIn("El ID del producto debe ser mayor que cero", result.errors)
    
    def test_empty_producto_id(self):
        """Test validation of empty product ID."""
        result = DatabaseValidator.validate_producto_id("")
        
        self.assertFalse(result.is_valid)
        self.assertIn("El ID del producto es obligatorio", result.errors)
    
    def test_valid_filename(self):
        """Test validation of valid filename."""
        result = DatabaseValidator.validate_filename("backup_2023.db")
        
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
    
    def test_invalid_filename(self):
        """Test validation of invalid filename."""
        result = DatabaseValidator.validate_filename("backup|file.db")
        
        self.assertFalse(result.is_valid)
        self.assertIn("El nombre del archivo contiene caracteres inválidos", result.errors)


class TestFilterValidator(unittest.TestCase):
    """Test cases for FilterValidator class."""
    
    def test_empty_filter(self):
        """Test validation of empty filter."""
        result = FilterValidator.validate_search_filter("")
        
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
    
    def test_valid_filter(self):
        """Test validation of valid filter."""
        result = FilterValidator.validate_search_filter("test filter")
        
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
    
    def test_long_filter(self):
        """Test validation of too long filter."""
        long_filter = "a" * 101
        result = FilterValidator.validate_search_filter(long_filter)
        
        self.assertFalse(result.is_valid)
        self.assertIn("El filtro de búsqueda es demasiado largo", result.errors)


class TestValidationResult(unittest.TestCase):
    """Test cases for ValidationResult class."""
    
    def test_valid_result(self):
        """Test creation of valid result."""
        result = ValidationResult(is_valid=True, errors=[])
        
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
    
    def test_invalid_result(self):
        """Test creation of invalid result."""
        errors = ["Error 1", "Error 2"]
        result = ValidationResult(is_valid=False, errors=errors)
        
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 2)
        self.assertEqual(result.errors[0], "Error 1")
        self.assertEqual(result.errors[1], "Error 2")


if __name__ == '__main__':
    unittest.main()