# Security Tests Directory

This directory contains comprehensive security tests for the Poetry Agents project, validating defensive security measures and vulnerability protections.

## Test Structure

### Core Security Tests
- **`test_security_fixes.py`** - Complete integration tests for all security fixes
- **`test_input_validation.py`** - Focused tests for input sanitization and validation
- **`test_error_handling.py`** - Tests for secure error handling and information disclosure prevention

### Test Runner
- **`run_security_tests.py`** - Comprehensive security test suite runner with reporting

### Documentation
- **`security_audit_log.md`** - Detailed security audit findings with specific line numbers
- **`security_recommendations.md`** - Implementation recommendations for security fixes

## Running Security Tests

### Run All Security Tests
```bash
cd tests/auto/security
python run_security_tests.py
```

### Run Individual Test Suites
```bash
# Input validation tests
python test_input_validation.py

# Error handling tests  
python test_error_handling.py

# Complete integration tests
python test_security_fixes.py
```

## Test Coverage

### Input Validation (`test_input_validation.py`)
- ✅ Prompt injection pattern detection (25+ patterns)
- ✅ Suspicious content filtering
- ✅ Model parameter validation
- ✅ Token limit enforcement
- ✅ Prompt length limits

### Error Handling (`test_error_handling.py`)
- ✅ Error message sanitization
- ✅ Information disclosure prevention
- ✅ Secure logging with redaction
- ✅ API error creation security
- ✅ Context preservation

### Integration Tests (`test_security_fixes.py`)
- ✅ End-to-end security validation
- ✅ LLM client security integration
- ✅ Real-world attack simulation
- ✅ Security utility validation

## Security Status

Current security test status: **🟢 100% PASS RATE**

All critical and high-priority security vulnerabilities have been addressed with comprehensive defensive measures.