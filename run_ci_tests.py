#!/usr/bin/env python3
"""
Simple script that runs the CI minimal tests directly
This is a more reliable approach for Jenkins CI as it doesn't depend on pytest
"""

import os
import sys
import unittest
from pathlib import Path

# Ensure we can import from the project
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

class SimpleTests(unittest.TestCase):
    """Basic tests that can run in any CI environment"""
    
    def test_python_version(self):
        """Test that we're using an acceptable Python version"""
        print(f"Python version: {sys.version}")
        self.assertTrue(
            sys.version_info >= (3, 8), 
            f"Python version {sys.version} should be 3.8+"
        )
    
    def test_ci_env(self):
        """Check CI environment"""
        ci_value = os.environ.get("CI", "").lower()
        print(f"CI environment variable: {ci_value}")
        # This is just informational, not a real test
        self.assertTrue(True)
    
    def test_essential_dirs(self):
        """Check that the essential directories exist"""
        for dirname in ["src", "tests", "tools"]:
            dir_path = project_root / dirname
            self.assertTrue(
                dir_path.is_dir(),
                f"Essential directory {dirname} should exist"
            )
    
    def test_essential_files(self):
        """Check that the essential files exist"""
        for filename in ["Jenkinsfile", "Makefile", "requirements.txt"]:
            file_path = project_root / filename
            self.assertTrue(
                file_path.is_file(),
                f"Essential file {filename} should exist"
            )
    
    def test_src_structure(self):
        """Check the src directory structure"""
        src_dir = project_root / "src"
        for filename in ["main.py", "config.py", "telegram_bot.py"]:
            file_path = src_dir / filename
            self.assertTrue(
                file_path.is_file(),
                f"Source file {filename} should exist"
            )

def run_tests():
    """Run the unit tests with a simple text runner"""
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleTests)
    result = unittest.TextTestRunner().run(suite)
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    print("=== Running Simple CI Tests ===")
    sys.exit(run_tests())
