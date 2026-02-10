"""
Controller module for inventory management system.
Handles business logic and coordinates between Model and View.
"""

from inventory_model import InventarioModel
from inventory_validation import ProductValidator
from inventory_config import Config
import logging


class InventoryController:
    """Controller class that manages application logic."""
    
    def __init__(self):
        """Initialize controller with model and configuration."""
        self.config = Config()
        self.model = InventarioModel(self.config.get('database', 'name'))
        self.validator = ProductValidator()
        self.ui = None
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=self.config.get('logging', 'level', 'INFO'),
            format=self.config.get('logging', 'format', '%(asctime)s - %(levelname)s - %(message)s'),
            filename=self.config.get('logging', 'file', 'inventory.log')
        )
        self.logger = logging.getLogger(__name__)
    
    def start_application(self):
        """Start inventory application."""
        try:
            self.logger.info("Starting inventory application")
            from inventory_ui import InventarioUI
            self.ui = InventarioUI(controller=self)
        except Exception as e:
            self.logger.error(f"Failed to start application: {e}")
            raise
    
    def add_product(self, nombre, cantidad, precio, stock_minimo=10):
        """Add a new product after validation."""
        try:
            # Validate input
            stock_minimo = stock_minimo or 10
            validation_result = self.validator.validate_product(nombre, cantidad, precio, stock_minimo)
            if not validation_result.is_valid:
                return {'success': False, 'errors': validation_result.errors}
            
            # Check for duplicates
            if self.model.producto_existe(nombre):
                return {'success': False, 'errors': [f"El producto '{nombre}' ya existe"]}
            
            # Add product
            self.model.agregar_producto(nombre, cantidad, precio, stock_minimo)
            self.logger.info(f"Product added: {nombre}")
            return {'success': True}
            
        except Exception as e:
            self.logger.error(f"Error adding product: {e}")
            return {'success': False, 'errors': [f"Error al agregar producto: {str(e)}"]}
    
    def update_product(self, producto_id, nombre, cantidad, precio, stock_minimo=None):
        """Update an existing product after validation."""
        try:
            # Validate input
            stock_minimo = stock_minimo or 10
            validation_result = self.validator.validate_product(nombre, cantidad, precio, stock_minimo)
            if not validation_result.is_valid:
                return {'success': False, 'errors': validation_result.errors}
            
            # Check for duplicates (excluding current product)
            if self.model.producto_existe(nombre, producto_id):
                return {'success': False, 'errors': [f"El producto '{nombre}' ya existe"]}
            
            # Update product
            self.model.actualizar_producto(producto_id, nombre, cantidad, precio, stock_minimo)
            self.logger.info(f"Product updated: {nombre} (ID: {producto_id})")
            return {'success': True}
            
        except Exception as e:
            self.logger.error(f"Error updating product: {e}")
            return {'success': False, 'errors': [f"Error al actualizar producto: {str(e)}"]}
    
    def delete_product(self, producto_id):
        """Delete a product after confirmation."""
        try:
            product = self.model.obtener_producto_por_id(producto_id)
            if not product:
                return {'success': False, 'errors': ['Producto no encontrado']}
            
            self.model.eliminar_producto(producto_id)
            self.logger.info(f"Product deleted: {product[1]} (ID: {producto_id})")
            return {'success': True}
            
        except Exception as e:
            self.logger.error(f"Error deleting product: {e}")
            return {'success': False, 'errors': [f"Error al eliminar producto: {str(e)}"]}
    
    def get_products(self, filtro=""):
        """Get all products, optionally filtered."""
        try:
            productos = self.model.obtener_productos()
            
            if filtro:
                productos = [p for p in productos if filtro.lower() in str(p[1]).lower()]
            
            return {'success': True, 'data': productos}
            
        except Exception as e:
            self.logger.error(f"Error getting products: {e}")
            return {'success': False, 'errors': [f"Error al obtener productos: {str(e)}"]}
    
    def get_product_by_id(self, producto_id):
        """Get a specific product by ID."""
        try:
            product = self.model.obtener_producto_por_id(producto_id)
            if product:
                return {'success': True, 'data': product}
            else:
                return {'success': False, 'errors': ['Producto no encontrado']}
                
        except Exception as e:
            self.logger.error(f"Error getting product: {e}")
            return {'success': False, 'errors': [f"Error al obtener producto: {str(e)}"]}
    
    def get_statistics(self):
        """Get inventory statistics."""
        try:
            stats = self.model.obtener_estadisticas()
            return {'success': True, 'data': stats}
            
        except Exception as e:
            self.logger.error(f"Error getting statistics: {e}")
            return {'success': False, 'errors': [f"Error al obtener estadísticas: {str(e)}"]}
    
    def get_low_stock_products(self):
        """Get products with low stock."""
        try:
            products = self.model.obtener_productos_bajo_stock()
            return {'success': True, 'data': products}
            
        except Exception as e:
            self.logger.error(f"Error getting low stock products: {e}")
            return {'success': False, 'errors': [f"Error al obtener productos con stock bajo: {str(e)}"]}
    
    def backup_database(self, backup_path):
        """Create a database backup."""
        try:
            success = self.model.backup_database(backup_path)
            if success:
                self.logger.info(f"Database backed up to: {backup_path}")
                return {'success': True}
            else:
                return {'success': False, 'errors': ['Error al crear copia de seguridad']}
                
        except Exception as e:
            self.logger.error(f"Error backing up database: {e}")
            return {'success': False, 'errors': [f"Error al crear copia de seguridad: {str(e)}"]}
    
    def restore_database(self, backup_path):
        """Restore database from backup."""
        try:
            success = self.model.restore_database(backup_path)
            if success:
                self.logger.info(f"Database restored from: {backup_path}")
                return {'success': True}
            else:
                return {'success': False, 'errors': ['Error al restaurar copia de seguridad']}
                
        except Exception as e:
            self.logger.error(f"Error restoring database: {e}")
            return {'success': False, 'errors': [f"Error al restaurar copia de seguridad: {str(e)}"]}
    
    def shutdown(self):
        """Clean shutdown of application."""
        try:
            if self.model and hasattr(self.model, 'conn'):
                self.model.conn.close()
            self.logger.info("Application shutdown complete")
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")