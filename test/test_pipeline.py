"""
Parallel Hash Cracking Engine - Pipeline Tests

Author: Sebastian Lodin
Date: November 2025
Description: Integration tests for pipeline components and workflow
"""

import unittest
import os
import json
from multiprocessing import Manager
from src.config_loader import ConfigLoader
from src.pipeline.receiver import Receiver
from src.pipeline.task_queue import TaskQueue
from src.pipeline.worker import Worker
from src.pipeline.collector import Collector


class TestPipeline(unittest.TestCase):
    """Test cases for pipeline components."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.test_csv = 'test/test_data.csv'
        cls.test_config = 'test/test_config.json'
        
        os.makedirs('test', exist_ok=True)
        
        with open(cls.test_csv, 'w', encoding='utf-8') as f:
            f.write('test1\n')
            f.write('test2\n')
            f.write('test3\n')
            f.write('hello\n')
            f.write('world\n')
            f.write('password\n')
            f.write('123456\n')
            f.write('admin\n')
            f.write('user\n')
            f.write('test\n')
        
        config = {
            "general": {
                "worker_count": 2,
                "chunk_size": 3,
                "max_workers": 4,
                "timeout_seconds": 30
            },
            "hash": {
                "algorithm": "SHA256",
                "pbkdf2_iterations": 100000,
                "pbkdf2_salt_length": 32
            },
            "input": {
                "csv_path": cls.test_csv,
                "csv_encoding": "utf-8",
                "csv_delimiter": ","
            },
            "output": {
                "log_path": "test/test.log",
                "results_path": "test/results.json",
                "verbose": False
            },
            "target": {
                "hash_to_find": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
            }
        }
        
        with open(cls.test_config, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test files."""
        if os.path.exists(cls.test_csv):
            os.remove(cls.test_csv)
        if os.path.exists(cls.test_config):
            os.remove(cls.test_config)
        if os.path.exists('test/test.log'):
            os.remove('test/test.log')
        if os.path.exists('test/results.json'):
            os.remove('test/results.json')
    
    def test_receiver_read_all(self):
        """Test receiver reads all records."""
        loader = ConfigLoader(self.test_config)
        config = loader.load()
        
        receiver = Receiver(config)
        records = receiver.read_all()
        
        self.assertEqual(len(records), 10)
        self.assertIn('test', records)
    
    def test_receiver_chunks(self):
        """Test receiver creates chunks."""
        loader = ConfigLoader(self.test_config)
        config = loader.load()
        
        receiver = Receiver(config)
        chunks = list(receiver.read_chunks())
        
        self.assertGreater(len(chunks), 0)
        self.assertLessEqual(len(chunks[0]), 3)
    
    def test_task_queue(self):
        """Test task queue operations."""
        queue = TaskQueue()
        
        queue.put(['test1', 'test2'])
        queue.put(['test3', 'test4'])
        
        task1 = queue.get()
        self.assertEqual(task1, ['test1', 'test2'])
        
        task2 = queue.get()
        self.assertEqual(task2, ['test3', 'test4'])
    
    def test_task_queue_poison_pill(self):
        """Test poison pill mechanism."""
        queue = TaskQueue()
        
        queue.send_poison_pills(2)
        
        pill1 = queue.get()
        pill2 = queue.get()
        
        self.assertIsNone(pill1)
        self.assertIsNone(pill2)
    
    def test_collector_results(self):
        """Test collector gathers results."""
        manager = Manager()
        results_dict = manager.dict()
        
        results_dict['match_0_1'] = {
            'worker_id': 0,
            'original': 'test',
            'hash': '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08',
            'algorithm': 'SHA256'
        }
        
        results = Collector.collect_results(results_dict)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['original'], 'test')


if __name__ == '__main__':
    unittest.main()
