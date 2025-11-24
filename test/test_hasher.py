import unittest
from src.pipeline.hasher import Hasher


class TestHasher(unittest.TestCase):
    """Test cases for Hasher class."""
    
    def test_sha256_hash(self):
        """Test SHA256 hashing."""
        hasher = Hasher('SHA256')
        
        result = hasher.hash('test')
        expected = '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'
        
        self.assertEqual(result, expected)
    
    def test_sha384_hash(self):
        """Test SHA384 hashing."""
        hasher = Hasher('SHA384')
        
        result = hasher.hash('test')
        expected = '768412320f7b0aa5812fce428dc4706b3cae50e02a64caa16a782249bfe8efc4b7ef1ccb126255d196047dfedf17a0a9'
        
        self.assertEqual(result, expected)
    
    def test_sha512_hash(self):
        """Test SHA512 hashing."""
        hasher = Hasher('SHA512')
        
        result = hasher.hash('test')
        expected = 'ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff'
        
        self.assertEqual(result, expected)
    
    def test_verify_sha256(self):
        """Test hash verification."""
        hasher = Hasher('SHA256')
        
        hash_value = '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'
        
        self.assertTrue(hasher.verify('test', hash_value))
        self.assertFalse(hasher.verify('wrong', hash_value))
    
    def test_quick_hash(self):
        """Test quick hash static method."""
        result = Hasher.quick_hash('test', 'SHA256')
        expected = '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'
        
        self.assertEqual(result, expected)
    
    def test_pbkdf2_hash(self):
        """Test PBKDF2 hashing."""
        hasher = Hasher('PBKDF2', iterations=1000)
        
        salt = b'test_salt_123456'
        result = hasher.hash('password', salt)
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 64)
    
    def test_invalid_algorithm(self):
        """Test invalid algorithm raises error."""
        with self.assertRaises(ValueError):
            Hasher('INVALID')
    
    def test_case_insensitive_verify(self):
        """Test verification is case insensitive."""
        hasher = Hasher('SHA256')
        
        hash_upper = '9F86D081884C7D659A2FEAA0C55AD015A3BF4F1B2B0B822CD15D6C15B0F00A08'
        hash_lower = '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'
        
        self.assertTrue(hasher.verify('test', hash_upper))
        self.assertTrue(hasher.verify('test', hash_lower))
    
    def test_empty_string_hash(self):
        """Test hashing empty string."""
        hasher = Hasher('SHA256')
        
        result = hasher.hash('')
        expected = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
