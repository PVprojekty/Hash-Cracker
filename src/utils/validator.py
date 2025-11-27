import re
from typing import Optional


class Validator:
    """Validation utilities for hash cracking engine."""
    
    @staticmethod
    def is_valid_hash(hash_value: str, algorithm: str) -> bool:
        """
        Check if hash string is valid for given algorithm.
        
        Args:
            hash_value: Hash string to validate
            algorithm: Hash algorithm (SHA256, SHA384, SHA512, PBKDF2)
        
        Returns:
            True if valid, False otherwise
        """
        if not hash_value or not isinstance(hash_value, str):
            return False
        
        # Remove whitespace and convert to lowercase
        hash_value = hash_value.strip().lower()
        
        if not hash_value:
            return False
        
        if algorithm == 'SHA256':
            return len(hash_value) == 64 and Validator._is_hex(hash_value)
        elif algorithm == 'SHA384':
            return len(hash_value) == 96 and Validator._is_hex(hash_value)
        elif algorithm == 'SHA512':
            return len(hash_value) == 128 and Validator._is_hex(hash_value)
        elif algorithm == 'PBKDF2':
            return len(hash_value) >= 64 and Validator._is_hex(hash_value)
        else:
            return False
    
    @staticmethod
    def _is_hex(value: str) -> bool:
        """Check if string contains only hexadecimal characters."""
        try:
            int(value, 16)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_birth_number(birth_number: str) -> bool:
        """
        Validate Czech birth number (rodné číslo).
        
        Args:
            birth_number: Birth number string (9 or 10 digits)
        
        Returns:
            True if valid format, False otherwise
        """
        if not birth_number or not isinstance(birth_number, str):
            return False
        
        birth_number = birth_number.replace('/', '').strip()
        
        if not birth_number.isdigit():
            return False
        
        if len(birth_number) not in [9, 10]:
            return False
        
        if len(birth_number) == 10:
            try:
                num = int(birth_number)
                if num % 11 != 0:
                    return False
            except ValueError:
                return False
        
        return True
    
    @staticmethod
    def normalize_birth_number(birth_number: str) -> Optional[str]:
        """
        Normalize birth number by removing slashes and whitespace.
        
        Args:
            birth_number: Birth number string
        
        Returns:
            Normalized birth number or None if invalid
        """
        if not birth_number:
            return None
        
        normalized = birth_number.replace('/', '').replace(' ', '').strip()
        
        if Validator.is_valid_birth_number(normalized):
            return normalized
        
        return None
    
    @staticmethod
    def is_valid_csv_line(line: str, expected_columns: int = 1) -> bool:
        """
        Check if CSV line has expected number of columns.
        
        Args:
            line: CSV line to validate
            expected_columns: Expected number of columns
        
        Returns:
            True if valid, False otherwise
        """
        if not line or not isinstance(line, str):
            return False
        
        line = line.strip()
        if not line:
            return False
        
        columns = line.split(',')
        return len(columns) >= expected_columns
