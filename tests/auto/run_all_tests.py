#!/usr/bin/env python3
"""
Comprehensive test runner for all auto tests
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import subprocess
import importlib.util
from pathlib import Path

def run_test_file(test_file_path):
    """
    Run a single test file and return success status
    
    Args:
        test_file_path: Path to the test file
        
    Returns:
        bool: True if test passed, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"Running: {test_file_path.name}")
    print('='*60)
    
    try:
        # Run the test file as a subprocess
        result = subprocess.run([
            sys.executable, str(test_file_path)
        ], capture_output=True, text=True, timeout=30)
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        # Check if test passed
        success = result.returncode == 0
        if success:
            print(f"✅ {test_file_path.name} PASSED")
        else:
            print(f"❌ {test_file_path.name} FAILED (return code: {result.returncode})")
            
        return success
        
    except subprocess.TimeoutExpired:
        print(f"⏰ {test_file_path.name} TIMED OUT")
        return False
    except Exception as e:
        print(f"💥 {test_file_path.name} ERROR: {e}")
        return False

def discover_and_run_tests():
    """Discover and run all test files in the auto directory"""
    
    # Get the tests/auto directory
    test_dir = Path(__file__).parent
    
    # Find all test files
    test_files = []
    for file_path in test_dir.glob("test_*.py"):
        # Skip this runner file
        if file_path.name != "run_all_tests.py":
            test_files.append(file_path)
    
    # Sort test files for consistent execution order
    test_files.sort()
    
    print("🚀 Poetry Agent Auto Test Suite")
    print("="*60)
    print(f"Found {len(test_files)} test files:")
    for test_file in test_files:
        print(f"  - {test_file.name}")
    
    # Run each test
    results = {}
    for test_file in test_files:
        results[test_file.name] = run_test_file(test_file)
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print('='*60)
    
    passed = sum(1 for success in results.values() if success)
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}  {test_name}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        return True
    else:
        print(f"⚠️  {total - passed} test(s) failed")
        return False

def run_priority_tests():
    """Run priority tests for refactored components"""
    priority_tests = [
        "test_base_llm_client.py",
        "test_llm_factory.py", 
        "test_enhancement_service.py",
        "test_gemini.py",
        "test_system.py"
    ]
    
    test_dir = Path(__file__).parent
    
    print("🎯 Running Priority Tests for Refactored Components")
    print("="*60)
    
    results = {}
    for test_name in priority_tests:
        test_path = test_dir / test_name
        if test_path.exists():
            results[test_name] = run_test_file(test_path)
        else:
            print(f"⚠️  Test file not found: {test_name}")
            results[test_name] = False
    
    # Summary
    passed = sum(1 for success in results.values() if success)
    total = len(results)
    
    print(f"\n🎯 Priority Test Results: {passed}/{total} tests passed")
    return passed == total

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Poetry Agent auto tests")
    parser.add_argument("--priority", action="store_true", 
                       help="Run only priority tests for refactored components")
    parser.add_argument("--full", action="store_true", default=True,
                       help="Run all auto tests (default)")
    
    args = parser.parse_args()
    
    if args.priority:
        success = run_priority_tests()
    else:
        success = discover_and_run_tests()
    
    sys.exit(0 if success else 1)