#!/usr/bin/env python3

import sys
import os
from multiprocessing import Manager, Semaphore
from typing import List

from src.config_loader import ConfigLoader
from src.pipeline.receiver import Receiver
from src.pipeline.task_queue import TaskQueue
from src.pipeline.worker import Worker
from src.pipeline.collector import Collector
from src.pipeline.logger import Logger
from src.utils.timer import Timer
from src.utils.validator import Validator


class HashCrackingPipeline:
    """Main pipeline orchestrator for parallel hash cracking."""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_loader = ConfigLoader(config_path)
        self.config = self.config_loader.load()
        
        self.logger = Logger(
            self.config['output']['log_path'],
            self.config['output']['verbose']
        )
        
        self.receiver = Receiver(self.config)
        self.task_queue = TaskQueue()
        self.manager = Manager()
        self.results_dict = self.manager.dict()
        
        self.worker_count = self.config['general']['worker_count']
        self.max_workers = self.config['general'].get('max_workers', 8)
        self.semaphore = Semaphore(min(self.worker_count, self.max_workers))
        
        self.workers: List[Worker] = []
        self.collector = None
        
        self.total_timer = Timer()
    
    def validate_setup(self) -> bool:
        """
        Validate pipeline setup and configuration.
        
        Returns:
            True if valid, False otherwise
        """
        self.logger.info("Validating pipeline setup...")
        
        if not self.receiver.validate_file():
            return False
        
        target_hash = self.config.get('target', {}).get('hash_to_find', '')
        
        if not target_hash:
            self.logger.warning("No target hash specified - will process but not find matches")
            return True
        
        algorithm = self.config['hash']['algorithm']
        
        if not Validator.is_valid_hash(target_hash, algorithm):
            self.logger.error(f"Invalid target hash for algorithm {algorithm}")
            return False
        
        self.logger.info("Validation passed")
        return True
    
    def create_workers(self, target_hash: str) -> None:
        """
        Create worker processes.
        
        Args:
            target_hash: Hash to search for
        """
        self.logger.info(f"Creating {self.worker_count} worker processes...")
        
        for i in range(self.worker_count):
            worker = Worker(
                worker_id=i,
                task_queue=self.task_queue,
                results_dict=self.results_dict,
                target_hash=target_hash,
                config=self.config
            )
            self.workers.append(worker)
        
        self.logger.info(f"Created {len(self.workers)} workers")
    
    def start_workers(self) -> None:
        """Start all worker processes."""
        self.logger.info("Starting worker processes...")
        
        for worker in self.workers:
            worker.start()
        
        self.logger.info(f"Started {len(self.workers)} workers")
    
    def load_data_to_queue(self) -> int:
        """
        Load CSV data into task queue.
        
        Returns:
            Number of chunks loaded
        """
        self.logger.info("Loading data into task queue...")
        
        chunk_count = 0
        
        for chunk in self.receiver.read_chunks():
            self.task_queue.put(chunk)
            chunk_count += 1
        
        self.logger.info(f"Loaded {chunk_count} chunks into queue")
        
        return chunk_count
    
    def wait_for_workers(self) -> None:
        """Wait for all workers to complete."""
        self.logger.info("Waiting for workers to complete...")
        
        for worker in self.workers:
            worker.join()
        
        self.logger.info("All workers completed")
    
    def run(self) -> bool:
        """
        Execute the complete pipeline.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info("="*60)
            self.logger.info("PARALLEL HASH CRACKING ENGINE")
            self.logger.info("="*60)
            
            if not self.validate_setup():
                self.logger.error("Setup validation failed")
                return False
            
            self.total_timer.start()
            
            target_hash = self.config.get('target', {}).get('hash_to_find', '')
            
            self.create_workers(target_hash)
            
            self.start_workers()
            
            chunks_loaded = self.load_data_to_queue()
            
            self.task_queue.send_poison_pills(self.worker_count)
            
            self.wait_for_workers()
            
            self.collector = Collector(self.results_dict, self.config)
            self.collector.start()
            self.collector.join()
            
            total_time = self.total_timer.stop()
            
            results = Collector.collect_results(self.results_dict)
            
            Collector.print_results(results, self.logger)
            
            stats = self.receiver.get_statistics()
            self.logger.log_pipeline_stats(
                total_time,
                stats['valid_lines'],
                len(results)
            )
            
            self.logger.info("="*60)
            self.logger.info("Pipeline completed successfully")
            self.logger.info("="*60)
            
            return True
        
        except KeyboardInterrupt:
            self.logger.warning("Pipeline interrupted by user")
            self._cleanup()
            return False
        
        except Exception as e:
            self.logger.error(f"Pipeline error: {e}")
            self._cleanup()
            return False
    
    def _cleanup(self) -> None:
        """Cleanup resources and terminate workers."""
        self.logger.info("Cleaning up...")
        
        for worker in self.workers:
            if worker.is_alive():
                worker.terminate()
                worker.join(timeout=5)
        
        if self.collector and self.collector.is_alive():
            self.collector.terminate()
            self.collector.join(timeout=5)


def main():
    """Main entry point."""
    config_path = "config.json"
    
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    
    pipeline = HashCrackingPipeline(config_path)
    
    success = pipeline.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
