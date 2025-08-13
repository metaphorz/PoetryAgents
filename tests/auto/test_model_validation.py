#!/usr/bin/env python3
"""
Test script to demonstrate the new OpenRouter model validation.
"""

from main import validate_openrouter_model, ask_user_to_continue_or_choose_another

def test_model_validation():
    """Test the model validation functionality."""
    
    print("🧪 Testing OpenRouter Model Validation\n")
    
    # Test with a free model (should trigger warnings)
    print("📋 Testing with a free model:")
    print("-" * 40)
    
    is_valid, warnings, alternatives = validate_openrouter_model("meta-llama/llama-3.2-11b-vision-instruct:free")
    
    if is_valid:
        print("✅ Model is valid")
        if warnings:
            print("⚠️  Warnings detected:")
            for warning in warnings:
                print(f"   {warning}")
        else:
            print("✅ No warnings")
    else:
        print("❌ Model validation failed:")
        for warning in warnings:
            print(f"   {warning}")
    
    print(f"\n🔄 Alternatives suggested: {alternatives}")
    
    print("\n" + "=" * 50 + "\n")
    
    # Test with a paid model (should be clean)
    print("📋 Testing with a paid model:")
    print("-" * 40)
    
    is_valid, warnings, alternatives = validate_openrouter_model("anthropic/claude-3.5-sonnet")
    
    if is_valid:
        print("✅ Model is valid")
        if warnings:
            print("⚠️  Warnings detected:")
            for warning in warnings:
                print(f"   {warning}")
        else:
            print("✅ No warnings")
    else:
        print("❌ Model validation failed:")
        for warning in warnings:
            print(f"   {warning}")
    
    print(f"\n🔄 Alternatives suggested: {alternatives}")

if __name__ == "__main__":
    test_model_validation()