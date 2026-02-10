"""
Configuration management for inventory system.
"""

import json
import os
from typing import Any, Dict, Optional


class Config:
    """Configuration manager for the inventory application."""
    
    def __init__(self, config_file: str = "config.json"):
        """Initialize configuration manager."""
        self.config_file = config_file
        self.config_data = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file or create default."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config file: {e}")
                self._create_default_config()
        else:
            self._create_default_config()
    
    def _create_default_config(self):
        """Create default configuration."""
        self.config_data = {
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
                "min_cantidad": 0,
                "max_cantidad": 999999,
                "min_precio": 0.0,
                "max_precio": 999999.99,
                "default_stock_minimo": 10
            },
            "logging": {
                "level": "INFO",
                "file": "inventory.log",
                "format": "%(asctime)s - %(levelname)s - %(message)s"
            },
            "export": {
                "csv_encoding": "utf-8",
                "pdf_page_size": "A4",
                "backup_retention_days": 30
            },
            "alerts": {
                "show_startup_alerts": True,
                "low_stock_threshold": 0.1,
                "critical_stock_threshold": 0.0
            }
        }
        self._save_config()
    
    def _save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving config file: {e}")
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        try:
            return self.config_data[section][key]
        except KeyError:
            return default
    
    def set(self, section: str, key: str, value: Any):
        """Set configuration value."""
        if section not in self.config_data:
            self.config_data[section] = {}
        self.config_data[section][key] = value
        self._save_config()
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire configuration section."""
        return self.config_data.get(section, {})
    
    def reload(self):
        """Reload configuration from file."""
        self._load_config()
    
    def validate_config(self) -> bool:
        """Validate configuration integrity."""
        required_sections = ["database", "ui", "validation", "logging"]
        
        for section in required_sections:
            if section not in self.config_data:
                return False
        
        # Validate database config
        db_config = self.config_data["database"]
        if not db_config.get("name"):
            return False
        
        return True