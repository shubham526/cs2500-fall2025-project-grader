#!/usr/bin/env python3
"""
CS 2500 Autograder Launcher
Run this from the project root to start grading
"""
import sys
from pathlib import Path

# Add src/core to Python path
project_root = Path(__file__).parent
core_dir = project_root / "src" / "core"
sys.path.insert(0, str(core_dir))

# Import and run
from src.core.autograder import main

if __name__ == "__main__":
    main()