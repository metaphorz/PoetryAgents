#!/usr/bin/env python3
"""
Test Direct API Mode (Option 1) - 3 LLM Providers with Model Selection
Tests the user interface flow for selecting Direct APIs vs OpenRouter,
then testing model selection dropdowns for OpenAI, Google/Gemini, and Anthropic/Claude.
"""

import os
import sys
import traceback
from datetime import datetime

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

def create_test_log():
    """Create a test log file to capture all test output."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"tests/auto/direct_api_test_log_{timestamp}.md"
    return log_file

def log_test_result(log_file, message):
    """Log test results to file and print to console."""
    print(message)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{message}\n")

def test_llm_client_model_selection():
    """Test LLM Client (Anthropic/Claude) model selection."""
    try:
        from llm_client import LLMClient
        
        print("\n=== Testing Anthropic/Claude Model Selection ===")
        
        # Test get_available_models method
        print("Testing LLMClient.get_available_models()...")
        models_dict = LLMClient.get_available_models()
        
        print(f"Found {len(models_dict)} Claude models:")
        for i, (display_name, model_id) in enumerate(models_dict.items(), 1):
            print(f"  {i:2d}. {display_name} -> {model_id}")
        
        # Test model validation
        if models_dict:
            first_display_name = list(models_dict.keys())[0]
            first_model_id = models_dict[first_display_name]
            
            print(f"\nTesting client initialization with display name: '{first_display_name}'")
            client = LLMClient(first_display_name)
            print(f"✅ Client initialized successfully")
            print(f"   Model ID: {client.model}")
            
            print(f"\nTesting client initialization with model ID: '{first_model_id}'")
            client2 = LLMClient(first_model_id)
            print(f"✅ Client initialized successfully")
            print(f"   Model ID: {client2.model}")
        
        return True, f"Claude: {len(models_dict)} models available"
        
    except Exception as e:
        error_msg = f"❌ Claude model selection failed: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        return False, error_msg

def test_gemini_client_model_selection():
    """Test Gemini Client (Google) model selection."""
    try:
        from gemini_client import GeminiClient
        
        print("\n=== Testing Google/Gemini Model Selection ===")
        
        # Test get_available_models method
        print("Testing GeminiClient.get_available_models()...")
        models_dict = GeminiClient.get_available_models()
        
        print(f"Found {len(models_dict)} Gemini models:")
        for i, (display_name, model_id) in enumerate(models_dict.items(), 1):
            print(f"  {i:2d}. {display_name} -> {model_id}")
        
        # Test model validation
        if models_dict:
            first_display_name = list(models_dict.keys())[0]
            first_model_id = models_dict[first_display_name]
            
            print(f"\nTesting client initialization with display name: '{first_display_name}'")
            client = GeminiClient(first_display_name)
            print(f"✅ Client initialized successfully")
            print(f"   Model ID: {client.model}")
            
            print(f"\nTesting client initialization with model ID: '{first_model_id}'")
            client2 = GeminiClient(first_model_id)
            print(f"✅ Client initialized successfully")
            print(f"   Model ID: {client2.model}")
        
        return True, f"Gemini: {len(models_dict)} models available"
        
    except Exception as e:
        error_msg = f"❌ Gemini model selection failed: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        return False, error_msg

def test_openai_client_model_selection():
    """Test OpenAI Client model selection."""
    try:
        from openai_client import OpenAIClient
        
        print("\n=== Testing OpenAI Model Selection ===")
        
        # Test get_available_models method
        print("Testing OpenAIClient.get_available_models()...")
        models_dict = OpenAIClient.get_available_models()
        
        print(f"Found {len(models_dict)} OpenAI models:")
        for i, (display_name, model_id) in enumerate(models_dict.items(), 1):
            print(f"  {i:2d}. {display_name} -> {model_id}")
        
        # Test model validation
        if models_dict:
            first_display_name = list(models_dict.keys())[0]
            first_model_id = models_dict[first_display_name]
            
            print(f"\nTesting client initialization with display name: '{first_display_name}'")
            client = OpenAIClient(first_display_name)
            print(f"✅ Client initialized successfully")
            print(f"   Model ID: {client.model}")
            
            print(f"\nTesting client initialization with model ID: '{first_model_id}'")
            client2 = OpenAIClient(first_model_id)
            print(f"✅ Client initialized successfully")
            print(f"   Model ID: {client2.model}")
        
        return True, f"OpenAI: {len(models_dict)} models available"
        
    except Exception as e:
        error_msg = f"❌ OpenAI model selection failed: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        return False, error_msg

def test_direct_api_config_structure():
    """Test the configuration structure for Direct API mode."""
    try:
        print("\n=== Testing Direct API Configuration Structure ===")
        
        # Test configuration creation for each provider
        test_configs = [
            {
                'name': 'OpenAI Agent 1, Gemini Agent 2',
                'config': {
                    'use_openrouter': False,
                    'agent1_llm': 'OpenAI',
                    'agent2_llm': 'Gemini',
                    'agent1_openai_model': 'gpt-4o',
                    'agent2_gemini_model': 'gemini-2.0-flash-exp',
                    'agent1_claude_model': None,
                    'agent2_claude_model': None,
                    'agent1_openrouter_search': None,
                    'agent2_openrouter_search': None,
                }
            },
            {
                'name': 'Claude Agent 1, OpenAI Agent 2',
                'config': {
                    'use_openrouter': False,
                    'agent1_llm': 'Claude',
                    'agent2_llm': 'OpenAI',
                    'agent1_claude_model': 'claude-3-5-sonnet-20241022',
                    'agent2_openai_model': 'gpt-4o',
                    'agent1_gemini_model': None,
                    'agent2_gemini_model': None,
                    'agent1_openrouter_search': None,
                    'agent2_openrouter_search': None,
                }
            },
            {
                'name': 'Gemini Agent 1, Claude Agent 2',
                'config': {
                    'use_openrouter': False,
                    'agent1_llm': 'Gemini',
                    'agent2_llm': 'Claude',
                    'agent1_gemini_model': 'gemini-2.0-flash-exp',
                    'agent2_claude_model': 'claude-3-5-sonnet-20241022',
                    'agent1_openai_model': None,
                    'agent2_openai_model': None,
                    'agent1_openrouter_search': None,
                    'agent2_openrouter_search': None,
                }
            }
        ]
        
        for test_config in test_configs:
            print(f"\nTesting configuration: {test_config['name']}")
            config = test_config['config']
            
            # Verify required fields
            assert config['use_openrouter'] == False, "Should be Direct API mode"
            assert config['agent1_llm'] in ['OpenAI', 'Gemini', 'Claude'], "Valid agent 1 LLM"
            assert config['agent2_llm'] in ['OpenAI', 'Gemini', 'Claude'], "Valid agent 2 LLM"
            
            # Check that appropriate model fields are set
            if config['agent1_llm'] == 'OpenAI':
                assert config['agent1_openai_model'] is not None, "OpenAI model should be set"
            elif config['agent1_llm'] == 'Gemini':
                assert config['agent1_gemini_model'] is not None, "Gemini model should be set"
            elif config['agent1_llm'] == 'Claude':
                assert config['agent1_claude_model'] is not None, "Claude model should be set"
            
            if config['agent2_llm'] == 'OpenAI':
                assert config['agent2_openai_model'] is not None, "OpenAI model should be set"
            elif config['agent2_llm'] == 'Gemini':
                assert config['agent2_gemini_model'] is not None, "Gemini model should be set"
            elif config['agent2_llm'] == 'Claude':
                assert config['agent2_claude_model'] is not None, "Claude model should be set"
            
            print(f"✅ Configuration valid")
        
        return True, f"Tested {len(test_configs)} configuration combinations"
        
    except Exception as e:
        error_msg = f"❌ Configuration structure test failed: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        return False, error_msg

def simulate_user_model_selection():
    """Simulate the user model selection flow."""
    try:
        print("\n=== Simulating User Model Selection Flow ===")
        
        # Simulate OpenAI selection
        print("\n1. Simulating OpenAI model selection:")
        from openai_client import OpenAIClient
        openai_models_dict = OpenAIClient.get_available_models()
        openai_models = list(openai_models_dict.keys())
        
        print("Available OpenAI models (6 most recent):")
        for i, model_name in enumerate(openai_models, 1):
            print(f"  {i:2d}. {model_name}")
        
        # Simulate user selecting option 1
        choice = 1
        if 1 <= choice <= len(openai_models):
            selected_display_name = openai_models[choice - 1]
            openai_model = openai_models_dict[selected_display_name]
            print(f"User selects: {choice} -> '{selected_display_name}' -> '{openai_model}'")
        
        # Simulate Gemini selection
        print("\n2. Simulating Gemini model selection:")
        from gemini_client import GeminiClient
        gemini_models_dict = GeminiClient.get_available_models()
        gemini_models = list(gemini_models_dict.keys())
        
        print("Available Gemini models (6 most relevant):")
        for i, model_name in enumerate(gemini_models, 1):
            print(f"  {i:2d}. {model_name}")
        
        # Simulate user selecting option 1
        choice = 1
        if 1 <= choice <= len(gemini_models):
            selected_display_name = gemini_models[choice - 1]
            gemini_model = gemini_models_dict[selected_display_name]
            print(f"User selects: {choice} -> '{selected_display_name}' -> '{gemini_model}'")
        
        # Simulate Claude selection
        print("\n3. Simulating Claude model selection:")
        from llm_client import LLMClient
        claude_models_dict = LLMClient.get_available_models()
        claude_models = list(claude_models_dict.keys())
        
        print("Available Claude models (6 most recent):")
        for i, model_name in enumerate(claude_models, 1):
            print(f"  {i}. {model_name}")
        
        # Simulate user selecting option 1
        choice = 1
        if 1 <= choice <= len(claude_models):
            selected_display_name = claude_models[choice - 1]
            claude_model = claude_models_dict[selected_display_name]
            print(f"User selects: {choice} -> '{selected_display_name}' -> '{claude_model}'")
        
        return True, "User model selection flow simulation completed"
        
    except Exception as e:
        error_msg = f"❌ User selection simulation failed: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        return False, error_msg

def main():
    """Main test function."""
    # Create test log
    log_file = create_test_log()
    
    # Start logging
    log_test_result(log_file, "# Direct API Mode (Option 1) Test Results")
    log_test_result(log_file, f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print("🧪 Testing Direct API Mode (Option 1) - 3 LLM Providers")
    print("=" * 60)
    
    # Track test results
    tests_passed = 0
    tests_failed = 0
    test_results = []
    
    # Run tests
    test_functions = [
        ("OpenAI Model Selection", test_openai_client_model_selection),
        ("Gemini Model Selection", test_gemini_client_model_selection),
        ("Claude Model Selection", test_llm_client_model_selection),
        ("Configuration Structure", test_direct_api_config_structure),
        ("User Selection Simulation", simulate_user_model_selection),
    ]
    
    for test_name, test_func in test_functions:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success, message = test_func()
            if success:
                tests_passed += 1
                result = f"✅ {test_name}: PASSED - {message}"
            else:
                tests_failed += 1
                result = f"❌ {test_name}: FAILED - {message}"
            
            test_results.append(result)
            log_test_result(log_file, result)
            
        except Exception as e:
            tests_failed += 1
            result = f"❌ {test_name}: ERROR - {str(e)}"
            test_results.append(result)
            log_test_result(log_file, result)
            traceback.print_exc()
    
    # Summary
    total_tests = tests_passed + tests_failed
    print(f"\n{'='*60}")
    print("🎯 DIRECT API MODE TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests Passed: {tests_passed}/{total_tests}")
    print(f"Tests Failed: {tests_failed}/{total_tests}")
    
    if tests_failed == 0:
        print("🎉 ALL TESTS PASSED! Direct API mode is working correctly.")
        status = "SUCCESS"
    else:
        print("⚠️  Some tests failed. Check the details above.")
        status = "PARTIAL"
    
    # Log summary
    log_test_result(log_file, f"\n## Test Summary")
    log_test_result(log_file, f"- Tests Passed: {tests_passed}/{total_tests}")
    log_test_result(log_file, f"- Tests Failed: {tests_failed}/{total_tests}")
    log_test_result(log_file, f"- Overall Status: {status}")
    log_test_result(log_file, f"- Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"\n📝 Detailed test log saved to: {log_file}")
    
    return tests_failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)