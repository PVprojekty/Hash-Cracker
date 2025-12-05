"""
Parallel Hash Cracking Engine - Hasher Module

Author: Sebastian Lodin
Date: November 2025
Description: Hash computation engine supporting multiple cryptographic algorithms
"""

import hashlib
import os
from typing import Optional


class Hasher:
    """Hash computation engine supporting multiple algorithms."""
    
    SUPPORTED_ALGORITHMS = ['SHA256', 'SHA384', 'SHA512', 'PBKDF2']
    
    def __init__(self, algorithm: str = 'SHA256', iterations: int = 100000, salt_length: int = 32):
        if algorithm not in self.SUPPORTED_ALGORITHMS:
            raise ValueError(f"Unsupported algorithm: {algorithm}. Must be one of {self.SUPPORTED_ALGORITHMS}")
        
        self.algorithm = algorithm
        self.iterations = iterations
        self.salt_length = salt_length
    
    def hash(self, data: str, salt: Optional[bytes] = None) -> str:
        """
        Compute cryptographic hash of given data.
        
        Args:
            data: String to hash
            salt: Optional salt for PBKDF2 (if None, random salt is generated)
        
        Returns:
            Hexadecimal hash string
        
        Raises:
            TypeError: If data is not a string
        """
        if not isinstance(data, str):
            raise TypeError(f"Data must be a string, got {type(data).__name__}")
        
        if self.algorithm == 'PBKDF2':
            return self._pbkdf2_hash(data, salt)
        else:
            return self._simple_hash(data)
    
    def _simple_hash(self, data: str) -> str:
        """Compute simple hash (SHA256/384/512)."""
        data_bytes = data.encode('utf-8')
        
        if self.algorithm == 'SHA256':
            return hashlib.sha256(data_bytes).hexdigest()
        elif self.algorithm == 'SHA384':
            return hashlib.sha384(data_bytes).hexdigest()
        elif self.algorithm == 'SHA512':
            return hashlib.sha512(data_bytes).hexdigest()
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")
    
    def _pbkdf2_hash(self, data: str, salt: Optional[bytes] = None) -> str:
        """Compute PBKDF2-HMAC-SHA256 hash."""
        if salt is None:
            salt = os.urandom(self.salt_length)
        
        data_bytes = data.encode('utf-8')
        key = hashlib.pbkdf2_hmac('sha256', data_bytes, salt, self.iterations)
        
        return salt.hex() + key.hex()
    
    def verify(self, data: str, hash_value: str) -> bool:
        """
        Verify if data matches given hash.
        
        Args:
            data: Original data to verify
            hash_value: Hash to compare against
        
        Returns:
            True if hash matches, False otherwise
        """
        if self.algorithm == 'PBKDF2':
            return self._verify_pbkdf2(data, hash_value)
        else:
            computed_hash = self._simple_hash(data)
            return computed_hash == hash_value.lower()
    
    def _verify_pbkdf2(self, data: str, hash_value: str) -> bool:
        """Verify PBKDF2 hash."""
        try:
            salt_hex = hash_value[:self.salt_length * 2]
            salt = bytes.fromhex(salt_hex)
            
            data_bytes = data.encode('utf-8')
            key = hashlib.pbkdf2_hmac('sha256', data_bytes, salt, self.iterations)
            
            expected_hash = salt.hex() + key.hex()
            return expected_hash == hash_value.lower()
        except (ValueError, IndexError):
            return False
    
    @staticmethod
    def quick_hash(data: str, algorithm: str = 'SHA256') -> str:
        """
        Quick hash computation without creating Hasher instance.
        
        Args:
            data: String to hash
            algorithm: Hash algorithm to use
        
        Returns:
            Hexadecimal hash string
        """
        hasher = Hasher(algorithm)
        return hasher.hash(data)
