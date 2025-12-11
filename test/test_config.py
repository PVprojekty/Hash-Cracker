"""
Parallel Hash Cracking Engine - Configuration Tests

Author: Sebastian Lodin
Date: November 2025
Description: Unit tests for configuration loader and validation
"""

import unittest
import json
import os
from src.config_loader import ConfigLoader


class TestConfig(unittest.TestCase):
    """Test cases for configuration loader."""
    
    def setUp(self):
        """Set up test configuration file."""
        self.test_config_path = 'test/test_config_loader.json'
        
        os.makedirs('test', exist_ok=True)
        
        self.valid_config = {
            "general": {
                "worker_count": 4,
                "chunk_size": 1000,
                "max_workers": 8,
                "timeout_seconds": 300
            },
            "hash": {
                "algorithm": "SHA256",
                "pbkdf2_iterations": 100000,
                "pbkdf2_salt_length": 32
            },
            "input": {
                "csv_path": "data/test.csv",
                "csv_encoding": "utf-8",
                "csv_delimiter": ","
            },
            "output": {
                "log_path": "logs/test.log",
                "results_path": "logs/results.json",
                "verbose": True
            }
        }
        
        with open(self.test_config_path, 'w', encoding='utf-8') as f:
            json.dump(self.valid_config, f)
    
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_config_path):
            os.remove(self.test_config_path)
    
    def test_load_valid_config(self):
        """Test loading valid configuration."""
        loader = ConfigLoader(self.test_config_path)
        config = loader.load()
        
        self.assertIsInstance(config, dict)
        self.assertIn('general', config)
        self.assertIn('hash', config)
    
    def test_get_nested_value(self):
        """Test getting nested configuration values."""
        loader = ConfigLoader(self.test_config_path)
        loader.load()
        
        worker_count = loader.get('general', 'worker_count')
        self.assertEqual(worker_count, 4)
        
        algorithm = loader.get('hash', 'algorithm')
        self.assertEqual(algorithm, 'SHA256')
    
    def test_get_default_value(self):
        """Test getting default value for missing key."""
        loader = ConfigLoader(self.test_config_path)
        loader.load()
        
        value = loader.get('nonexistent', 'key', default='default_value')
        self.assertEqual(value, 'default_value')
    
    def test_set_value(self):
        """Test setting configuration value."""
        loader = ConfigLoader(self.test_config_path)
        loader.load()
        
        loader.set(8, 'general', 'worker_count')
        
        value = loader.get('general', 'worker_count')
        self.assertEqual(value, 8)
    
    def test_invalid_worker_count(self):
        """Test validation fails for invalid worker count."""
        invalid_config = self.valid_config.copy()
        invalid_config['general']['worker_count'] = 0
        
        invalid_path = 'test/invalid_config.json'
        
        with open(invalid_path, 'w', encoding='utf-8') as f:
            json.dump(invalid_config, f)
        
        loader = ConfigLoader(invalid_path)
        
        with self.assertRaises(ValueError):
            loader.load()
        
        os.remove(invalid_path)
    
    def test_invalid_algorithm(self):
        """Test validation fails for invalid algorithm."""
        invalid_config = self.valid_config.copy()
        invalid_config['hash']['algorithm'] = 'INVALID'
        
        invalid_path = 'test/invalid_algorithm.json'
        
        with open(invalid_path, 'w', encoding='utf-8') as f:
            json.dump(invalid_config, f)
        
        loader = ConfigLoader(invalid_path)
        
        with self.assertRaises(ValueError):
            loader.load()
        
        os.remove(invalid_path)
    
    def test_missing_file(self):
        """Test error when configuration file is missing."""
        loader = ConfigLoader('nonexistent.json')
        
        with self.assertRaises(FileNotFoundError):
            loader.load()


if __name__ == '__main__':
    unittest.main()
