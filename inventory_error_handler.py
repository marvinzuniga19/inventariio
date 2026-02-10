"""
Error handling and exception management for inventory system.
"""

import logging
import traceback
from typing import Dict, Any, Optional, List
from functools import wraps


class InventoryError(Exception):
    """Base exception for inventory system."""
    
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "GENERIC_ERROR"
        self.details = details or {}


class ValidationError(InventoryError):
    """Exception for validation errors."""
    
    def __init__(self, message: str, field: str = None, value: Any = None):
        super().__init__(message, "VALIDATION_ERROR")
        self.field = field
        self.value = value


class DatabaseError(InventoryError):
    """Exception for database errors."""
    
    def __init__(self, message: str, operation: str = None, query: str = None):
        super().__init__(message, "DATABASE_ERROR")
        self.operation = operation
        self.query = query


class ConfigurationError(InventoryError):
    """Exception for configuration errors."""
    
    def __init__(self, message: str, config_key: str = None):
        super().__init__(message, "CONFIG_ERROR")
        self.config_key = config_key


class UIError(InventoryError):
    """Exception for UI-related errors."""
    
    def __init__(self, message: str, component: str = None):
        super().__init__(message, "UI_ERROR")
        self.component = component


class ErrorHandler:
    """Centralized error handling for the application."""
    
    def __init__(self, logger: logging.Logger = None):
        """Initialize error handler with optional logger."""
        self.logger = logger or logging.getLogger(__name__)
        self.error_callbacks = {}
    
    def register_callback(self, error_code: str, callback):
        """Register a callback for specific error types."""
        self.error_callbacks[error_code] = callback
    
    def handle_exception(self, exception: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle an exception and return a standardized error response."""
        context = context or {}
        
        # Log the exception
        self.logger.error(f"Exception occurred: {str(exception)}")
        self.logger.debug(f"Traceback: {traceback.format_exc()}")
        
        # Handle specific exception types
        if isinstance(exception, InventoryError):
            return self._handle_inventory_error(exception, context)
        elif isinstance(exception, ValueError):
            return self._handle_value_error(exception, context)
        elif isinstance(exception, IOError):
            return self._handle_io_error(exception, context)
        else:
            return self._handle_generic_error(exception, context)
    
    def _handle_inventory_error(self, error: InventoryError, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle inventory-specific errors."""
        response = {
            'success': False,
            'error_code': error.error_code,
            'message': error.message,
            'type': 'inventory_error'
        }
        
        if error.details:
            response['details'] = error.details
        
        # Add field-specific information for validation errors
        if isinstance(error, ValidationError) and error.field:
            response['field'] = error.field
            response['invalid_value'] = str(error.value) if error.value is not None else None
        
        # Add operation information for database errors
        if isinstance(error, DatabaseError) and error.operation:
            response['operation'] = error.operation
        
        # Add context information
        response.update(context)
        
        # Execute callback if registered
        if error.error_code in self.error_callbacks:
            try:
                self.error_callbacks[error.error_code](error, response)
            except Exception as callback_error:
                self.logger.error(f"Error in callback for {error.error_code}: {callback_error}")
        
        return response
    
    def _handle_value_error(self, error: ValueError, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle value errors."""
        response = {
            'success': False,
            'error_code': 'VALUE_ERROR',
            'message': f"Error de valor: {str(error)}",
            'type': 'value_error'
        }
        response.update(context)
        return response
    
    def _handle_io_error(self, error: IOError, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle I/O errors."""
        response = {
            'success': False,
            'error_code': 'IO_ERROR',
            'message': f"Error de entrada/salida: {str(error)}",
            'type': 'io_error'
        }
        response.update(context)
        return response
    
    def _handle_generic_error(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle generic errors."""
        response = {
            'success': False,
            'error_code': 'GENERIC_ERROR',
            'message': f"Error inesperado: {str(error)}",
            'type': 'generic_error'
        }
        response.update(context)
        return response


def safe_execute(error_handler: ErrorHandler = None):
    """Decorator for safe execution of functions."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                handler = error_handler or ErrorHandler()
                context = {
                    'function': func.__name__,
                    'module': func.__module__,
                    'args': str(args),
                    'kwargs': str(kwargs)
                }
                return handler.handle_exception(e, context)
        return wrapper
    return decorator


def validate_and_execute(error_handler: ErrorHandler = None):
    """Decorator for validation and safe execution."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            handler = error_handler or ErrorHandler()
            context = {
                'function': func.__name__,
                'module': func.__module__
            }
            
            try:
                # Execute function
                result = func(*args, **kwargs)
                
                # Validate result if it has validation errors
                if isinstance(result, dict) and 'success' in result and not result['success']:
                    if 'errors' in result:
                        raise ValidationError(
                            message=f"Validation failed: {'; '.join(result['errors'])}",
                            error_code="VALIDATION_FAILED",
                            details={'validation_errors': result['errors']}
                        )
                
                return result
                
            except Exception as e:
                return handler.handle_exception(e, context)
        
        return wrapper
    return decorator