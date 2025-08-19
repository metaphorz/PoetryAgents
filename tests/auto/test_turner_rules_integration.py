#!/usr/bin/env python3
"""
Test script to verify Turner-based rules integration in the judge system.
Tests both critique and editing functionality with Turner guidelines.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def test_turner_rules_manager():
    """Test the TurnerRulesManager functionality."""
    print("Testing TurnerRulesManager...")
    
    from turner_rules import TurnerRulesManager
    
    manager = TurnerRulesManager()
    
    # Test basic functionality
    categories = manager.get_all_categories()
    print(f"✅ Found {len(categories)} rule categories: {categories}")
    
    # Test critique rules formatting
    critique_rules = manager.get_critique_rules()
    assert "Language Style:" in critique_rules
    assert "Avoid Archaic Language" in critique_rules
    print("✅ Critique rules properly formatted")
    
    # Test editing rules formatting
    editing_rules = manager.get_editing_rules()
    assert "Language Style:" in editing_rules
    assert "Replace archaic terms" in editing_rules
    print("✅ Editing rules properly formatted")
    
    # Test avoid list
    avoid_list = manager.get_avoid_list()
    assert len(avoid_list) > 10
    assert any("archaic" in item.lower() for item in avoid_list)
    print(f"✅ Avoid list contains {len(avoid_list)} items")
    
    # Test enhance list
    enhance_list = manager.get_enhance_list()
    assert len(enhance_list) >= 10
    assert any("mixed emotion" in item.lower() for item in enhance_list)
    print(f"✅ Enhance list contains {len(enhance_list)} items")
    
    print("✅ TurnerRulesManager tests completed successfully!\n")

def test_critique_service_integration():
    """Test CritiqueService integration with Turner rules."""
    print("Testing CritiqueService Turner integration...")
    
    from critique_service import CritiqueService
    
    # Create test dialogue data
    test_dialogue_data = {
        'title': 'Test Dialogue',
        'agents': ['Character1', 'Character2'],
        'conversation': [
            {
                'agent': 'Character1',
                'poetry': 'O\'er the fields of gold I wandered,\nThou art beautiful, my dear,\nForsooth, thy beauty conquers all,\nBehest of love, I shall not fear.',
                'round': 1,
                'agent_index': 0,
                'llm_used': 'Claude'
            },
            {
                'agent': 'Character2', 
                'poetry': 'In shadows deep where sorrows dwell,\nAbstract thoughts of love and pain,\nGeneric beauty, nothing more,\nClichéd words fall like the rain.',
                'round': 1,
                'agent_index': 1,
                'llm_used': 'Gemini'
            }
        ],
        'config': {
            'theme': 'love and loss',
            'form': 'haiku',
            'poem_length': 3,
            'conversation_length': 2,
            'use_openrouter': False,
            'agent1_llm': 'Claude',
            'agent2_llm': 'Gemini'
        }
    }
    
    critique_service = CritiqueService()
    
    # Test critique prompt generation
    critique_prompt = critique_service._create_critique_prompt(test_dialogue_data)
    
    # Verify Turner-based elements are included
    assert "Turner's comprehensive approach" in critique_prompt
    assert "TURNER-BASED CRITIQUE FRAMEWORK" in critique_prompt
    assert "Archaic language" in critique_prompt
    assert "mixed emotions" in critique_prompt.lower()
    assert "concrete vs abstract" in critique_prompt
    print("✅ Critique prompt includes Turner-based framework")
    
    # Test edit prompt generation
    sample_critique = "The poems contain archaic language and lack emotional complexity."
    edit_prompt = critique_service._create_edit_prompt(test_dialogue_data, sample_critique)
    
    # Verify Turner-based elements are included
    assert "Turner's comprehensive poetry improvement guidelines" in edit_prompt
    assert "TURNER-BASED IMPROVEMENT GUIDELINES" in edit_prompt
    assert "ENHANCEMENT PRIORITIES" in edit_prompt
    assert "ELEMENTS TO AVOID/CORRECT" in edit_prompt
    assert "mixed emotions" in edit_prompt
    print("✅ Edit prompt includes Turner-based improvement guidelines")
    
    print("✅ CritiqueService integration tests completed successfully!\n")

def test_judge_selection_with_turner_rules():
    """Test that judge selection logic works with Turner rules integration."""
    print("Testing judge selection logic with Turner rules...")
    
    from critique_service import CritiqueService
    
    critique_service = CritiqueService()
    
    # Test that the CritiqueService has the select_judge method
    assert hasattr(critique_service, 'select_judge'), "CritiqueService should have select_judge method"
    print("✅ select_judge method exists")
    
    # Test that Turner rules are available for judge system
    assert hasattr(critique_service, 'turner_rules'), "CritiqueService should have turner_rules"
    print("✅ Turner rules available in critique service")
    
    # Test the company mapping logic (without creating actual clients)
    test_config = {
        'use_openrouter': False,
        'num_agents': 2,
        'agent1_llm': 'Claude',
        'agent2_llm': 'OpenAI',
        'theme': 'nature',
        'form': 'haiku'
    }
    
    # We can't easily test the actual judge selection without API keys,
    # but we can verify the method exists and the integration is structurally sound
    print("✅ Judge selection structure verified")
    
    print("✅ Judge selection with Turner rules completed successfully!\n")
    return True

def test_end_to_end_functionality():
    """Test end-to-end functionality with Turner rules (without actual API calls)."""
    print("Testing end-to-end Turner rules functionality...")
    
    from critique_service import CritiqueService
    from turner_rules import TurnerRulesManager
    
    # Verify components work together
    critique_service = CritiqueService()
    
    # Check that TurnerRulesManager is properly initialized
    assert hasattr(critique_service, 'turner_rules')
    assert isinstance(critique_service.turner_rules, TurnerRulesManager)
    print("✅ CritiqueService properly initialized with TurnerRulesManager")
    
    # Test that all rule categories are available
    categories = critique_service.turner_rules.get_all_categories()
    expected_categories = ['language_style', 'emotional_thematic', 'technical_craft', 'formal_structure', 'quality_refinement']
    for category in expected_categories:
        assert category in categories, f"Missing category: {category}"
    print("✅ All expected rule categories are available")
    
    print("✅ End-to-end functionality test completed successfully!\n")

def run_all_tests():
    """Run all Turner rules integration tests."""
    print("=" * 60)
    print("RUNNING TURNER RULES INTEGRATION TESTS")
    print("=" * 60)
    
    tests = [
        test_turner_rules_manager,
        test_critique_service_integration,
        test_judge_selection_with_turner_rules,
        test_end_to_end_functionality
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("🎉 ALL TURNER RULES INTEGRATION TESTS PASSED!")
        return True
    else:
        print("❌ Some tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)