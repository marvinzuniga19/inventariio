"""
Unit tests for configuration management.
"""

import unittest
import os
import tempfile
import json
from inventory_config import Config


class TestConfig(unittest.TestCase):
    """Test cases for Config class."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_config = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
        self.test_config.close()
        self.config = Config(self.test_config.name)
    
    def tearDown(self):
        """Clean up test environment."""
        os.unlink(self.test_config.name)
    
    def test_default_config_creation(self):
        """Test creation of default configuration."""
        # Check if default sections exist
        self.assertIn("database", self.config.config_data)
        self.assertIn("ui", self.config.config_data)
        self.assertIn("validation", self.config.config_data)
        self.assertIn("logging", self.config.config_data)
    
    def test_get_config_value(self):
        """Test getting configuration values."""
        # Test existing value
        db_name = self.config.get("database", "name")
        self.assertEqual(db_name, "inventario.db")
        
        # Test non-existing value with default
        non_existing = self.config.get("nonexistent", "key", "default_value")
        self.assertEqual(non_existing, "default_value")
    
    def test_set_config_value(self):
        """Test setting configuration values."""
        # Set a new value
        self.config.set("test_section", "test_key", "test_value")
        
        # Verify it was set
        value = self.config.get("test_section", "test_key")
        self.assertEqual(value, "test_value")
        
        # Verify it was saved to file
        new_config = Config(self.test_config.name)
        saved_value = new_config.get("test_section", "test_key")
        self.assertEqual(saved_value, "test_value")
    
    def test_get_section(self):
        """Test getting entire configuration section."""
        db_section = self.config.get_section("database")
        
        self.assertIsInstance(db_section, dict)
        self.assertIn("name", db_section)
        self.assertIn("backup_folder", db_section)
    
    def test_validate_config(self):
        """Test configuration validation."""
        # Valid config should pass
        self.assertTrue(self.config.validate_config())
        
        # Create invalid config file
        invalid_config = {"invalid": "config"}
        with open(self.test_config.name, 'w') as f:
            json.dump(invalid_config, f)
        
        # Reload and validate
        self.config.reload()
        self.assertFalse(self.config.validate_config())
    
    def test_load_existing_config(self):
        """Test loading existing configuration file."""
        # Create a custom config
        custom_config = {
            "database": {"name": "custom.db"},
            "ui": {"theme": "dark"}
        }
        with open(self.test_config.name, 'w') as f:
            json.dump(custom_config, f)
        
        # Load config
        config = Config(self.test_config.name)
        
        # Verify custom values were loaded
        self.assertEqual(config.get("database", "name"), "custom.db")
        self.assertEqual(config.get("ui", "theme"), "dark")


if __name__ == '__main__':
    unittest.main()