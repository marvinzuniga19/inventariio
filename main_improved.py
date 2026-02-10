"""
Main entry point for the inventory management system.
Uses MVC architecture with proper error handling.
"""

import sys
import logging
from inventory_controller import InventoryController
from inventory_error_handler import ErrorHandler, InventoryError
import traceback


def setup_logging():
    """Setup basic logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('inventory.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def handle_critical_error(error):
    """Handle critical errors that prevent application startup."""
    print(f"❌ Error crítico: {error}")
    print("El sistema no pudo iniciarse correctamente.")
    print("Revise el archivo de log para más detalles: inventory.log")
    logging.critical(f"Critical error during startup: {error}")
    logging.critical(f"Traceback: {traceback.format_exc()}")
    sys.exit(1)


def main():
    """Main application entry point."""
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        
        logger.info("=" * 50)
        logger.info("Iniciando Sistema de Gestión de Inventario")
        logger.info("=" * 50)
        
        # Initialize error handler
        error_handler = ErrorHandler(logger)
        
        # Register error callbacks
        error_handler.register_callback("DATABASE_ERROR", lambda err, resp: 
            logger.error(f"Database error in {resp.get('operation', 'unknown')}: {err.message}"))
        
        error_handler.register_callback("VALIDATION_ERROR", lambda err, resp:
            logger.warning(f"Validation error for field {err.field}: {err.message}"))
        
        error_handler.register_callback("CONFIG_ERROR", lambda err, resp:
            logger.error(f"Configuration error for {err.config_key}: {err.message}"))
        
        # Initialize and start application
        logger.info("Inicializando controlador de la aplicación...")
        controller = InventoryController()
        
        logger.info("Iniciando interfaz de usuario...")
        controller.start_application()
        
    except KeyboardInterrupt:
        print("\n👋 Aplicación terminada por el usuario")
        logger.info("Application terminated by user")
        
    except InventoryError as e:
        handle_critical_error(e)
        
    except Exception as e:
        handle_critical_error(f"Error inesperado: {e}")
        
    finally:
        # Cleanup
        try:
            if 'controller' in locals():
                controller.shutdown()
                logger.info("Application shutdown complete")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")


if __name__ == "__main__":
    main()