"""
Unit tests for inventory model.
"""

import unittest
import os
import tempfile
import sqlite3
from inventory_model import InventarioModel


class TestInventoryModel(unittest.TestCase):
    """Test cases for InventarioModel class."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.test_db.close()
        self.model = InventarioModel(self.test_db.name)
    
    def tearDown(self):
        """Clean up test environment."""
        self.model.conn.close()
        os.unlink(self.test_db.name)
    
    def test_database_initialization(self):
        """Test database and table creation."""
        # Check if table exists
        self.model.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='productos'"
        )
        result = self.model.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'productos')
    
    def test_add_product(self):
        """Test adding a new product."""
        result = self.model.agregar_producto("Test Product", 10, 99.99, 5)
        
        # Verify product was added
        products = self.model.obtener_productos()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0][1], "Test Product")
        self.assertEqual(products[0][2], 10)
        self.assertEqual(products[0][3], 99.99)
        self.assertEqual(products[0][4], 5)
    
    def test_get_product_by_id(self):
        """Test retrieving a product by ID."""
        # Add a product first
        self.model.agregar_producto("Test Product", 10, 99.99, 5)
        
        # Get the product
        products = self.model.obtener_productos()
        product_id = products[0][0]
        
        retrieved = self.model.obtener_producto_por_id(product_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved[1], "Test Product")
    
    def test_update_product(self):
        """Test updating an existing product."""
        # Add a product first
        self.model.agregar_producto("Test Product", 10, 99.99, 5)
        products = self.model.obtener_productos()
        product_id = products[0][0]
        
        # Update the product
        self.model.actualizar_producto(product_id, "Updated Product", 20, 199.99, 15)
        
        # Verify update
        updated = self.model.obtener_producto_por_id(product_id)
        self.assertEqual(updated[1], "Updated Product")
        self.assertEqual(updated[2], 20)
        self.assertEqual(updated[3], 199.99)
        self.assertEqual(updated[4], 15)
    
    def test_delete_product(self):
        """Test deleting a product."""
        # Add a product first
        self.model.agregar_producto("Test Product", 10, 99.99, 5)
        products = self.model.obtener_productos()
        self.assertEqual(len(products), 1)
        product_id = products[0][0]
        
        # Delete the product
        self.model.eliminar_producto(product_id)
        
        # Verify deletion
        products = self.model.obtener_productos()
        self.assertEqual(len(products), 0)
    
    def test_producto_existe(self):
        """Test checking if product exists."""
        # Add a product
        self.model.agregar_producto("Test Product", 10, 99.99, 5)
        
        # Test existence
        self.assertTrue(self.model.producto_existe("Test Product"))
        self.assertFalse(self.model.producto_existe("Nonexistent Product"))
        
        # Test with exclusion
        products = self.model.obtener_productos()
        product_id = products[0][0]
        self.assertFalse(self.model.producto_existe("Test Product", product_id))
    
    def test_obtener_estadisticas(self):
        """Test getting inventory statistics."""
        # Add test products
        self.model.agregar_producto("Product 1", 10, 100.0, 5)
        self.model.agregar_producto("Product 2", 20, 200.0, 15)
        self.model.agregar_producto("Product 3", 5, 50.0, 10)  # Low stock
        
        stats = self.model.obtener_estadisticas()
        
        self.assertEqual(stats['total_productos'], 3)
        self.assertEqual(stats['valor_total'], 5250.0)  # 1000 + 4000 + 250
        self.assertEqual(stats['bajo_stock'], 1)  # Product 3 has low stock
        self.assertEqual(stats['stock_total'], 35)  # 10 + 20 + 5
    
    def test_obtener_productos_bajo_stock(self):
        """Test getting products with low stock."""
        # Add test products
        self.model.agregar_producto("Normal Product", 20, 100.0, 10)
        self.model.agregar_producto("Low Stock Product", 5, 200.0, 10)
        
        low_stock_products = self.model.obtener_productos_bajo_stock()
        
        self.assertEqual(len(low_stock_products), 1)
        self.assertEqual(low_stock_products[0][1], "Low Stock Product")
    
    def test_backup_restore(self):
        """Test database backup and restore."""
        # Add a product
        self.model.agregar_producto("Backup Test", 15, 75.0, 5)
        
        # Create backup
        backup_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        backup_file.close()
        
        try:
            # Backup
            self.model.backup_database(backup_file.name)
            self.assertTrue(os.path.exists(backup_file.name))
            
            # Delete product from original database
            products = self.model.obtener_productos()
            product_id = products[0][0]
            self.model.eliminar_producto(product_id)
            
            # Verify deletion
            products_after_delete = self.model.obtener_productos()
            self.assertEqual(len(products_after_delete), 0)
            
            # Restore from backup
            self.model.restore_database(backup_file.name)
            
            # Verify restoration
            products_after_restore = self.model.obtener_productos()
            self.assertEqual(len(products_after_restore), 1)
            self.assertEqual(products_after_restore[0][1], "Backup Test")
            
        finally:
            # Clean up
            if os.path.exists(backup_file.name):
                os.unlink(backup_file.name)


if __name__ == '__main__':
    unittest.main()