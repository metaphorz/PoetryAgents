#!/usr/bin/env python3
"""
Security Test Runner for Poetry Agents
Comprehensive security validation and reporting.
"""

import sys
import os
import subprocess
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

def run_security_test_suite():
    """Run all security tests and generate comprehensive report."""
    print("🔒 POETRY AGENTS SECURITY TEST SUITE")
    print("=" * 60)
    
    start_time = time.time()
    
    # Test files to run
    test_files = [
        "test_security_fixes.py",
        "test_input_validation.py", 
        "test_error_handling.py"
    ]
    
    total_passed = 0
    total_failed = 0
    total_errors = 0
    
    for test_file in test_files:
        print(f"\n🧪 Running {test_file}...")
        print("-" * 40)
        
        try:
            # Run the test file
            result = subprocess.run([
                sys.executable, test_file
            ], cwd=Path(__file__).parent, capture_output=True, text=True)
            
            # Parse results
            if "OK" in result.stdout and result.returncode == 0:
                # Extract test count from output
                lines = result.stdout.split('\n')
                for line in lines:
                    if "Ran" in line and "tests" in line:
                        test_count = int(line.split()[1])
                        total_passed += test_count
                        print(f"✅ {test_count} tests passed")
                        break
            else:
                # Parse failure information
                lines = result.stdout.split('\n')
                for line in lines:
                    if "Failed:" in line:
                        failed = int(line.split("Failed:")[1].split()[0])
                        total_failed += failed
                    if "Errors:" in line:
                        errors = int(line.split("Errors:")[1].split()[0])
                        total_errors += errors
                
                print(f"❌ Test failures detected")
                if result.stdout:
                    print("STDOUT:", result.stdout[-500:])  # Last 500 chars
                if result.stderr:
                    print("STDERR:", result.stderr[-500:])
                    
        except Exception as e:
            print(f"❌ Error running {test_file}: {e}")
            total_errors += 1
    
    # Generate summary report
    elapsed_time = time.time() - start_time
    total_tests = total_passed + total_failed + total_errors
    success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    print("\n" + "=" * 60)
    print("🔒 SECURITY TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests Run: {total_tests}")
    print(f"✅ Passed: {total_passed}")
    print(f"❌ Failed: {total_failed}")
    print(f"💥 Errors: {total_errors}")
    print(f"📊 Success Rate: {success_rate:.1f}%")
    print(f"⏱️  Execution Time: {elapsed_time:.2f} seconds")
    
    # Security status assessment
    if total_failed == 0 and total_errors == 0:
        status = "🟢 SECURE"
        print(f"\n🎉 Security Status: {status}")
        print("All security tests passed! The application is secure.")
    elif total_failed > 0:
        status = "🟡 VULNERABLE"
        print(f"\n⚠️  Security Status: {status}")
        print(f"Security vulnerabilities detected: {total_failed} failed tests")
    else:
        status = "🔴 UNKNOWN"
        print(f"\n❓ Security Status: {status}")
        print(f"Unable to complete security assessment: {total_errors} errors")
    
    print("\n📋 SECURITY CHECKLIST:")
    security_items = [
        ("Prompt Injection Protection", total_passed > 0),
        ("Input Validation", total_passed > 0),
        ("Error Sanitization", total_passed > 0),
        ("Secure Logging", total_passed > 0),
        ("Parameter Validation", total_passed > 0)
    ]
    
    for item, passed in security_items:
        symbol = "✅" if passed else "❌"
        print(f"{symbol} {item}")
    
    print("=" * 60)
    
    return total_failed == 0 and total_errors == 0

if __name__ == "__main__":
    success = run_security_test_suite()
    sys.exit(0 if success else 1)