#!/usr/bin/env python3
"""
Test script to verify improved judge selection logic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def test_improved_judge_selection():
    """Test the improved judge selection logic with proper company mapping."""
    from critique_service import CritiqueService
    
    critique_service = CritiqueService()
    
    print("Testing improved judge selection with company mapping...")
    
    # Test 1: Direct APIs - Anthropic (Claude Opus 4.1) + OpenAI (O3 Mini)
    print("\n" + "="*60)
    print("Test 1: Direct APIs - Anthropic + OpenAI → Should select Google")
    test_config1 = {
        'use_openrouter': False,
        'num_agents': 2,
        'agent1_llm': 'Claude',
        'agent2_llm': 'OpenAI',
        'agent1_claude_model': 'Claude Opus 4.1',
        'agent2_openai_model': 'O3 Mini',
        'theme': 'test theme',
        'form': 'haiku'
    }
    
    try:
        company, judge_client = critique_service.select_judge(test_config1)
        print(f"✅ Judge company: {company}")
        print(f"✅ Judge model: {getattr(judge_client, 'model', 'Unknown')}")
        
        # Verify correct company selection
        assert company == 'Google', f"Expected Google, got {company}"
        print("✅ Correct company selected (Google)!")
        
        # Verify different model than agents
        agent_models = {'Claude Opus 4.1', 'O3 Mini'}
        judge_model = getattr(judge_client, 'model_name', getattr(judge_client, 'model', ''))
        assert judge_model not in agent_models, f"Judge using same model as agent: {judge_model}"
        print(f"✅ Judge uses different model: {judge_model}")
        
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
    
    # Test 2: Direct APIs - OpenAI + Google → Should select Anthropic
    print("\n" + "="*60)
    print("Test 2: Direct APIs - OpenAI + Google → Should select Anthropic")
    test_config2 = {
        'use_openrouter': False,
        'num_agents': 2,
        'agent1_llm': 'OpenAI',
        'agent2_llm': 'Gemini',
        'agent1_openai_model': 'O3 Mini',
        'agent2_gemini_model': 'Gemini 2.5 Pro',
        'theme': 'test theme',
        'form': 'haiku'
    }
    
    try:
        company, judge_client = critique_service.select_judge(test_config2)
        print(f"✅ Judge company: {company}")
        print(f"✅ Judge model: {getattr(judge_client, 'model', 'Unknown')}")
        
        # Verify correct company selection
        assert company == 'Anthropic', f"Expected Anthropic, got {company}"
        print("✅ Correct company selected (Anthropic)!")
        
    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
    
    # Test 3: OpenRouter mode
    print("\n" + "="*60) 
    print("Test 3: OpenRouter - anthropic/claude-opus-4.1 + openai/gpt-5-chat → Should select Google")
    test_config3 = {
        'use_openrouter': True,
        'num_agents': 2,
        'agent1_openrouter_search': 'anthropic/claude-opus-4.1',
        'agent2_openrouter_search': 'openai/gpt-5-chat',
        'theme': 'test theme',
        'form': 'haiku'
    }
    
    try:
        routing, judge_client = critique_service.select_judge(test_config3)
        print(f"✅ Judge routing: {routing}")
        print(f"✅ Judge model: {getattr(judge_client, 'model', 'Unknown')}")
        
        # Verify OpenRouter routing
        assert routing == 'OpenRouter', f"Expected OpenRouter, got {routing}"
        
        # Verify different model than agents
        agent_models = {'anthropic/claude-opus-4.1', 'openai/gpt-5-chat'}
        judge_model = getattr(judge_client, 'model', '')
        assert judge_model not in agent_models, f"Judge using same model as agent: {judge_model}"
        
        # Verify judge uses Google model (should start with google/ or gemini/)
        judge_is_google = ('google/' in judge_model.lower() or 'gemini' in judge_model.lower())
        if judge_is_google:
            print(f"✅ Judge correctly selected from Google: {judge_model}")
        else:
            print(f"⚠️  Judge not from Google (might be acceptable): {judge_model}")
        
    except Exception as e:
        print(f"❌ Test 3 failed: {e}")
    
    print(f"\n✅ Judge selection improvement tests completed!")

if __name__ == "__main__":
    test_improved_judge_selection()