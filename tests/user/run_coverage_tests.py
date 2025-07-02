"""
Comprehensive test runner with coverage analysis for all Python modules.
"""

import unittest
import sys
import os
import coverage
import subprocess

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def run_all_coverage_tests():
    """Run all tests with coverage analysis."""
    print("🧪 Starting comprehensive unit tests with coverage analysis...")
    print("=" * 80)
    
    # Initialize coverage
    cov = coverage.Coverage(
        source=['.'],
        omit=[
            'tests/*',
            'demo_run.py',  # Demo script
            '*/site-packages/*',
            '*/__pycache__/*'
        ]
    )
    
    # Start coverage measurement
    cov.start()
    
    try:
        # Discover and run all tests in the user directory
        test_dir = os.path.dirname(os.path.abspath(__file__))
        loader = unittest.TestLoader()
        suite = loader.discover(test_dir, pattern='test_coverage_*.py')
        
        # Run tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # Stop coverage measurement
        cov.stop()
        cov.save()
        
        print("\n" + "=" * 80)
        print("📊 COVERAGE ANALYSIS")
        print("=" * 80)
        
        # Print coverage report
        print("\nCoverage Summary:")
        cov.report(show_missing=True)
        
        # Generate HTML coverage report
        html_dir = os.path.join(os.path.dirname(test_dir), 'coverage_html_report')
        cov.html_report(directory=html_dir)
        print(f"\n📄 Detailed HTML coverage report generated: {html_dir}/index.html")
        
        print("\n" + "=" * 80)
        print("🎯 TEST RESULTS SUMMARY")
        print("=" * 80)
        
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
        
        if result.failures:
            print("\n❌ FAILURES:")
            for test, traceback in result.failures:
                print(f"  - {test}")
                print(f"    {traceback.splitlines()[-1] if traceback.splitlines() else 'No details'}")
        
        if result.errors:
            print("\n🚨 ERRORS:")
            for test, traceback in result.errors:
                print(f"  - {test}")
                print(f"    {traceback.splitlines()[-1] if traceback.splitlines() else 'No details'}")
        
        if result.wasSuccessful():
            print("\n✅ ALL TESTS PASSED!")
        else:
            print(f"\n❌ {len(result.failures + result.errors)} test(s) failed")
        
        return result.wasSuccessful()
        
    except Exception as e:
        cov.stop()
        print(f"\n🚨 Error running tests: {e}")
        import traceback
        traceback.print_exc()
        return False


def analyze_module_coverage():
    """Analyze coverage for each individual module."""
    modules = [
        'main.py',
        'character_names.py', 
        'llm_client.py',
        'gemini_client.py',
        'prompts.py',
        'dialogue_manager.py'
    ]
    
    print("\n" + "=" * 80)
    print("📋 MODULE-BY-MODULE COVERAGE ANALYSIS")
    print("=" * 80)
    
    for module in modules:
        print(f"\n🔍 Testing {module}:")
        
        # Run coverage for specific module
        try:
            result = subprocess.run([
                'python', '-m', 'coverage', 'run', '--source=.', 
                f'tests/user/test_coverage_{module.replace(".py", "")}.py'
            ], capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            
            if result.returncode == 0:
                print("  ✅ Tests passed")
            else:
                print("  ❌ Tests failed")
                if result.stderr:
                    print(f"     Error: {result.stderr.strip()}")
        except Exception as e:
            print(f"  🚨 Error: {e}")


def check_code_quality():
    """Check for potential code quality issues."""
    print("\n" + "=" * 80)
    print("🔍 CODE QUALITY CHECKS")
    print("=" * 80)
    
    issues = []
    
    # Check for TODO comments
    todo_count = 0
    for root, dirs, files in os.walk('.'):
        if 'tests' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.split('\n')
                        for i, line in enumerate(lines, 1):
                            if 'TODO' in line.upper() or 'FIXME' in line.upper():
                                issues.append(f"TODO/FIXME in {filepath}:{i} - {line.strip()}")
                                todo_count += 1
                except Exception:
                    pass
    
    print(f"📝 TODO/FIXME comments found: {todo_count}")
    
    # Check for long lines (>120 characters)
    long_lines = 0
    for root, dirs, files in os.walk('.'):
        if 'tests' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines, 1):
                            if len(line.rstrip()) > 120:
                                long_lines += 1
                except Exception:
                    pass
    
    print(f"📏 Long lines (>120 chars): {long_lines}")
    
    if issues:
        print("\n🔍 Issues found:")
        for issue in issues[:10]:  # Show first 10 issues
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more")
    else:
        print("✅ No major code quality issues found")


if __name__ == '__main__':
    print("🚀 Poetry Agent Dialogue Generator - Comprehensive Test Suite")
    print("=" * 80)
    
    success = run_all_coverage_tests()
    analyze_module_coverage()
    check_code_quality()
    
    print("\n" + "=" * 80)
    print("🏁 TESTING COMPLETE")
    print("=" * 80)
    
    if success:
        print("🎉 All tests passed successfully!")
        exit(0)
    else:
        print("💥 Some tests failed. Please review the output above.")
        exit(1)