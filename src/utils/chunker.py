"""
Parallel Hash Cracking Engine - Chunker Utility

Author: Sebastian Lodin
Date: November 2025
Description: Data chunking utilities for efficient parallel processing
"""

from typing import List, Any, Iterator


class Chunker:
    """Split data into chunks for parallel processing."""
    
    @staticmethod
    def chunk_list(data: List[Any], chunk_size: int) -> Iterator[List[Any]]:
        """
        Split list into chunks of specified size.
        
        Args:
            data: List to chunk
            chunk_size: Maximum size of each chunk
        
        Yields:
            Chunks of data
        """
        if chunk_size < 1:
            raise ValueError("chunk_size must be at least 1")
        
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]
    
    @staticmethod
    def chunk_range(start: int, end: int, chunk_size: int) -> Iterator[tuple]:
        """
        Generate range chunks for distributed processing.
        
        Args:
            start: Start of range (inclusive)
            end: End of range (exclusive)
            chunk_size: Size of each chunk
        
        Yields:
            Tuples of (chunk_start, chunk_end)
        """
        if chunk_size < 1:
            raise ValueError("chunk_size must be at least 1")
        
        current = start
        while current < end:
            chunk_end = min(current + chunk_size, end)
            yield (current, chunk_end)
            current = chunk_end
    
    @staticmethod
    def distribute_work(total_items: int, num_workers: int) -> List[tuple]:
        """
        Distribute work evenly among workers.
        
        Args:
            total_items: Total number of items to process
            num_workers: Number of workers
        
        Returns:
            List of (start, end) tuples for each worker
        """
        if num_workers < 1:
            raise ValueError("num_workers must be at least 1")
        
        if total_items < 1:
            return []
        
        chunk_size = total_items // num_workers
        remainder = total_items % num_workers
        
        distribution = []
        start = 0
        
        for i in range(num_workers):
            extra = 1 if i < remainder else 0
            end = start + chunk_size + extra
            
            if start < total_items:
                distribution.append((start, end))
            
            start = end
        
        return distribution
