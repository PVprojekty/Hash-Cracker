#!/usr/bin/env python3
"""
Parallel Hash Cracking Engine - Quick Start Script

Author: Sebastian Lodin
Date: November 2025
Description: Convenient launcher script with default configuration
"""

import sys
import os

# Add parent directory to path so we can import src
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from src.main import main

if __name__ == "__main__":
    print("=" * 60)
    print("PARALLEL HASH CRACKING ENGINE - Quick Start")
    print("=" * 60)
    print()
    print("This will run the engine with default configuration.")
    print("To find 'test' in data/sample_data.csv")
    print()
    
    # Override sys.argv to use default config
    sys.argv = ['run.py', 'config.json']
    
    main()
