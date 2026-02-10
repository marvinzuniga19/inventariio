"""
Test runner for inventory management system.
"""

import sys
import os
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test modules
from test_inventory_model import TestInventoryModel
from test_validation import TestProductValidator, TestDatabaseValidator, TestFilterValidator, TestValidationResult
from test_config import TestConfig


def run_all_tests():
    """Run all unit tests."""
    # Create test suite
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(loader.loadTestsFromTestCase(TestInventoryModel))
    test_suite.addTest(loader.loadTestsFromTestCase(TestProductValidator))
    test_suite.addTest(loader.loadTestsFromTestCase(TestDatabaseValidator))
    test_suite.addTest(loader.loadTestsFromTestCase(TestFilterValidator))
    test_suite.addTest(loader.loadTestsFromTestCase(TestValidationResult))
    test_suite.addTest(loader.loadTestsFromTestCase(TestConfig))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Return result
    return result.wasSuccessful()


if __name__ == '__main__':
    print("Running Inventory Management System Tests")
    print("=" * 50)
    
    success = run_all_tests()
    
    print("=" * 50)
    if success:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)