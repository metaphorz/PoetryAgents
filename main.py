#!/usr/bin/env python3
"""
Poetry Agent Dialogue System
Main entry point for the poetry dialogue generator.
"""

def get_user_input():
    """Collect the required questions from the user."""
    print("Welcome to Poetry Agent Dialogue Generator!")
    print("Please answer the following questions:\n")
    
    # Initial Choice: API Mode
    print("Choose your LLM access method:")
    print("  1. Direct APIs (Claude, Gemini, OpenAI) - More model options per provider")
    print("  2. OpenRouter API - Access to 100+ models from many providers")
    
    while True:
        api_mode = input("Select mode (1 or 2): ").strip()
        if api_mode in ['1', '2']:
            use_openrouter = (api_mode == '2')
            break
        else:
            print("Please enter '1' or '2'")
    
    print()
    
    # Model Selection (right after API mode choice)
    if use_openrouter:
        # OpenRouter path: free-form model search with numbered selection
        print("2. Choose model for Agent 1")
        print("   🔗 Browse all available models: https://openrouter.ai/models")
        print("   💡 Tip: Use the 'Filter models' feature on the website to explore options")
        print("   Enter search term like 'Claude', 'OpenAI', 'Baidu', 'Llama', 'Mistral', etc.")
        
        while True:
            model1_search = input("2a. Model search for Agent 1: ").strip()
            if model1_search:
                # Get search results
                from openrouter_client import OpenRouterClient
                matches = OpenRouterClient.search_models(model1_search)
                if matches:
                    if len(matches) == 1:
                        print(f"Found 1 match: {matches[0]['id']}")
                        
                        # Validate the model
                        is_valid, warnings, alternatives = validate_openrouter_model(matches[0]['id'])
                        if not is_valid:
                            print("\n".join(warnings))
                            continue
                        
                        if warnings:
                            continue_with_model, new_model_id = ask_user_to_continue_or_choose_another(
                                matches[0]['id'], warnings, alternatives
                            )
                            if continue_with_model and new_model_id:
                                llm1_choice = 'OpenRouter'
                                agent1_openrouter_search = new_model_id
                                print(f"✅ Using model: {new_model_id}")
                                break
                            elif not continue_with_model:
                                continue  # Go back to search
                        else:
                            llm1_choice = 'OpenRouter'
                            agent1_openrouter_search = matches[0]['id']
                            break
                    else:
                        print(f"Found {len(matches)} matches:")
                        for i, match in enumerate(matches, 1):
                            print(f"  {i:2d}. {match['id']}")
                            if match.get('description'):
                                print(f"      {match['description'][:80]}...")
                        
                        while True:
                            try:
                                choice = int(input(f"Select model (1-{len(matches)}): ").strip())
                                if 1 <= choice <= len(matches):
                                    selected_model = matches[choice - 1]
                                    print(f"Selected: {selected_model['id']}")
                                    
                                    # Validate the selected model
                                    is_valid, warnings, alternatives = validate_openrouter_model(selected_model['id'])
                                    if not is_valid:
                                        print("\n".join(warnings))
                                        continue
                                    
                                    if warnings:
                                        continue_with_model, new_model_id = ask_user_to_continue_or_choose_another(
                                            selected_model['id'], warnings, alternatives
                                        )
                                        if continue_with_model and new_model_id:
                                            llm1_choice = 'OpenRouter'
                                            agent1_openrouter_search = new_model_id
                                            print(f"✅ Using model: {new_model_id}")
                                            break
                                        elif not continue_with_model:
                                            continue  # Go back to model selection
                                    else:
                                        llm1_choice = 'OpenRouter'
                                        agent1_openrouter_search = selected_model['id']
                                        break
                                else:
                                    print(f"Please enter a number between 1 and {len(matches)}")
                            except ValueError:
                                print("Please enter a valid number")
                        break
                else:
                    print("No matches found. Try a different search term (e.g., 'Claude', 'OpenAI', 'Google').")
            else:
                print("Please enter a search term.")

        # Agent 2 selection for OpenRouter
        print("\n3. Choose model for Agent 2")
        print("   🔗 Browse all available models: https://openrouter.ai/models")
        print("   💡 Tip: Use the 'Filter models' feature on the website to explore options")
        print("   Enter search term like 'Claude', 'OpenAI', 'Baidu', 'Llama', 'Mistral', etc.")
        
        while True:
            model2_search = input("3a. Model search for Agent 2: ").strip()
            if model2_search:
                # Get search results
                from openrouter_client import OpenRouterClient
                matches = OpenRouterClient.search_models(model2_search)
                if matches:
                    if len(matches) == 1:
                        print(f"Found 1 match: {matches[0]['id']}")
                        
                        # Validate the model
                        is_valid, warnings, alternatives = validate_openrouter_model(matches[0]['id'])
                        if not is_valid:
                            print("\n".join(warnings))
                            continue
                        
                        if warnings:
                            continue_with_model, new_model_id = ask_user_to_continue_or_choose_another(
                                matches[0]['id'], warnings, alternatives
                            )
                            if continue_with_model and new_model_id:
                                llm2_choice = 'OpenRouter'
                                agent2_openrouter_search = new_model_id
                                print(f"✅ Using model: {new_model_id}")
                                break
                            elif not continue_with_model:
                                continue  # Go back to search
                        else:
                            llm2_choice = 'OpenRouter'
                            agent2_openrouter_search = matches[0]['id']
                            break
                    else:
                        print(f"Found {len(matches)} matches:")
                        for i, match in enumerate(matches, 1):
                            print(f"  {i:2d}. {match['id']}")
                            if match.get('description'):
                                print(f"      {match['description'][:80]}...")
                        
                        while True:
                            try:
                                choice = int(input(f"Select model (1-{len(matches)}): ").strip())
                                if 1 <= choice <= len(matches):
                                    selected_model = matches[choice - 1]
                                    print(f"Selected: {selected_model['id']}")
                                    
                                    # Validate the selected model
                                    is_valid, warnings, alternatives = validate_openrouter_model(selected_model['id'])
                                    if not is_valid:
                                        print("\n".join(warnings))
                                        continue
                                    
                                    if warnings:
                                        continue_with_model, new_model_id = ask_user_to_continue_or_choose_another(
                                            selected_model['id'], warnings, alternatives
                                        )
                                        if continue_with_model and new_model_id:
                                            llm2_choice = 'OpenRouter'
                                            agent2_openrouter_search = new_model_id
                                            print(f"✅ Using model: {new_model_id}")
                                            break
                                        elif not continue_with_model:
                                            continue  # Go back to model selection
                                    else:
                                        llm2_choice = 'OpenRouter'
                                        agent2_openrouter_search = selected_model['id']
                                        break
                                else:
                                    print(f"Please enter a number between 1 and {len(matches)}")
                            except ValueError:
                                print("Please enter a valid number")
                        break
                else:
                    print("No matches found. Try a different search term (e.g., 'Claude', 'OpenAI', 'Google').")
            else:
                print("Please enter a search term.")
                
        # Set model variables to None for OpenRouter
        claude1_model = None
        gemini1_model = None
        openai1_model = None
        claude2_model = None
        gemini2_model = None
        openai2_model = None
        
    else:
        # Direct API path: choose from 3 providers for Agent 1
        while True:
            llm1_choice = input("2. Which LLM should Agent 1 use? (Claude/Gemini/OpenAI) ").strip().title()
            if llm1_choice in ['Claude', 'Gemini', 'Openai']:
                if llm1_choice == 'Openai':
                    llm1_choice = 'OpenAI'  # Normalize to proper case
                break
            else:
                print("Please enter 'Claude', 'Gemini', or 'OpenAI'.")
        
        agent1_openrouter_search = None

        # Model selection for Agent 1 (Direct APIs)
        claude1_model = None
        gemini1_model = None
        openai1_model = None
        
        if llm1_choice == 'Claude':
            from llm_client import LLMClient
            claude_models_dict = LLMClient.get_available_models()
            claude_models = list(claude_models_dict.keys())
            print("Available Claude models (6 most recent):")
            for i, model_name in enumerate(claude_models, 1):
                print(f"  {i}. {model_name}")
            
            while True:
                try:
                    choice = int(input("2a. Which Claude model for Agent 1? (enter number): ").strip())
                    if 1 <= choice <= len(claude_models):
                        selected_display_name = claude_models[choice - 1]
                        claude1_model = claude_models_dict[selected_display_name]
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(claude_models)}")
                except ValueError:
                    print("Please enter a valid number")

        elif llm1_choice == 'Gemini':
            from gemini_client import GeminiClient
            gemini_models_dict = GeminiClient.get_available_models()
            gemini_models = list(gemini_models_dict.keys())
            print("Available Gemini models (6 most relevant):")
            for i, model_name in enumerate(gemini_models, 1):
                print(f"  {i:2d}. {model_name}")
            
            while True:
                try:
                    choice = int(input("2a. Which Gemini model for Agent 1? (enter number): ").strip())
                    if 1 <= choice <= len(gemini_models):
                        selected_display_name = gemini_models[choice - 1]
                        gemini1_model = gemini_models_dict[selected_display_name]
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(gemini_models)}")
                except ValueError:
                    print("Please enter a valid number")

        elif llm1_choice == 'OpenAI':
            from openai_client import OpenAIClient
            openai_models_dict = OpenAIClient.get_available_models()
            openai_models = list(openai_models_dict.keys())
            print("Available OpenAI models (6 most recent):")
            for i, model_name in enumerate(openai_models, 1):
                print(f"  {i:2d}. {model_name}")
            
            while True:
                try:
                    choice = int(input("2a. Which OpenAI model for Agent 1? (enter number): ").strip())
                    if 1 <= choice <= len(openai_models):
                        selected_display_name = openai_models[choice - 1]
                        openai1_model = openai_models_dict[selected_display_name]
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(openai_models)}")
                except ValueError:
                    print("Please enter a valid number")

        # Agent 2 selection for Direct APIs
        while True:
            llm2_choice = input("3. Which LLM should Agent 2 use? (Claude/Gemini/OpenAI) ").strip().title()
            if llm2_choice in ['Claude', 'Gemini', 'Openai']:
                if llm2_choice == 'Openai':
                    llm2_choice = 'OpenAI'  # Normalize to proper case
                break
            else:
                print("Please enter 'Claude', 'Gemini', or 'OpenAI'.")
        
        agent2_openrouter_search = None

        # Model selection for Agent 2 (Direct APIs)
        claude2_model = None
        gemini2_model = None
        openai2_model = None
        
        if llm2_choice == 'Claude':
            from llm_client import LLMClient
            claude_models_dict = LLMClient.get_available_models()
            claude_models = list(claude_models_dict.keys())
            print("Available Claude models (6 most recent):")
            for i, model_name in enumerate(claude_models, 1):
                print(f"  {i}. {model_name}")
            
            while True:
                try:
                    choice = int(input("3a. Which Claude model for Agent 2? (enter number): ").strip())
                    if 1 <= choice <= len(claude_models):
                        selected_display_name = claude_models[choice - 1]
                        claude2_model = claude_models_dict[selected_display_name]
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(claude_models)}")
                except ValueError:
                    print("Please enter a valid number")

        elif llm2_choice == 'Gemini':
            from gemini_client import GeminiClient
            gemini_models_dict = GeminiClient.get_available_models()
            gemini_models = list(gemini_models_dict.keys())
            print("Available Gemini models (6 most relevant):")
            for i, model_name in enumerate(gemini_models, 1):
                print(f"  {i:2d}. {model_name}")
            
            while True:
                try:
                    choice = int(input("3a. Which Gemini model for Agent 2? (enter number): ").strip())
                    if 1 <= choice <= len(gemini_models):
                        selected_display_name = gemini_models[choice - 1]
                        gemini2_model = gemini_models_dict[selected_display_name]
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(gemini_models)}")
                except ValueError:
                    print("Please enter a valid number")

        elif llm2_choice == 'OpenAI':
            from openai_client import OpenAIClient
            openai_models_dict = OpenAIClient.get_available_models()
            openai_models = list(openai_models_dict.keys())
            print("Available OpenAI models (6 most recent):")
            for i, model_name in enumerate(openai_models, 1):
                print(f"  {i:2d}. {model_name}")
            
            while True:
                try:
                    choice = int(input("3a. Which OpenAI model for Agent 2? (enter number): ").strip())
                    if 1 <= choice <= len(openai_models):
                        selected_display_name = openai_models[choice - 1]
                        openai2_model = openai_models_dict[selected_display_name]
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(openai_models)}")
                except ValueError:
                    print("Please enter a valid number")
    
    print()
    
    # Question 4: Theme
    theme = input("4. What is the theme? ")
    
    # Always use 2 agents
    num_agents = 2
    
    # Question 5: Form of dialogue
    valid_forms = ['haiku', 'prose', 'sonnet', 'villanelle', 'limerick', 'ballad', 'ghazal', 'tanka']
    while True:
        print("Available forms: haiku, prose, sonnet, villanelle, limerick, ballad, ghazal, tanka")
        form = input("5. What is the form of dialogue? ").lower().strip()
        if form in valid_forms:
            break
        else:
            print(f"Please enter one of: {', '.join(valid_forms)}")
    
    # Question 6: Length of each poem (form-dependent)
    fixed_forms = {
        'haiku': 3,
        'sonnet': 14, 
        'villanelle': 19,
        'limerick': 5,
        'tanka': 5
    }
    
    if form in fixed_forms:
        poem_length = fixed_forms[form]
        length_unit = 'lines'
        print(f"6. Poem length: {poem_length} {length_unit} (traditional {form})")
    else:
        # Variable forms need user input
        if form == 'ballad':
            while True:
                try:
                    poem_length = int(input("6. How many stanzas for each ballad? "))
                    if poem_length > 0:
                        length_unit = 'stanzas'
                        break
                    else:
                        print("Please enter a positive number.")
                except ValueError:
                    print("Please enter a valid number.")
        elif form == 'ghazal':
            while True:
                try:
                    poem_length = int(input("6. How many couplets for each ghazal? (5-15 recommended) "))
                    if poem_length > 0:
                        length_unit = 'couplets'
                        break
                    else:
                        print("Please enter a positive number.")
                except ValueError:
                    print("Please enter a valid number.")
        elif form == 'prose':
            while True:
                try:
                    poem_length = int(input("6. How many paragraphs for each prose piece? "))
                    if poem_length > 0:
                        length_unit = 'paragraphs'
                        break
                    else:
                        print("Please enter a positive number.")
                except ValueError:
                    print("Please enter a valid number.")
        else:
            # Fallback for any new forms
            while True:
                try:
                    poem_length = int(input("6. What is the length of each poem? "))
                    if poem_length > 0:
                        length_unit = 'lines'
                        break
                    else:
                        print("Please enter a positive number.")
                except ValueError:
                    print("Please enter a valid number.")
    
    # Question 7: Length of conversation (clarified as rounds)
    while True:
        try:
            conversation_length = int(input("7. How many rounds of conversation? (each agent will write one poem per round) "))
            if conversation_length > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Question 8: Emoji preference
    while True:
        emoji_choice = input("8. Add emojis to enhance the poetry? (yes/no) ").lower().strip()
        if emoji_choice in ['yes', 'y', 'no', 'n']:
            use_emojis = emoji_choice in ['yes', 'y']
            break
        else:
            print("Please enter 'yes' or 'no'.")
    
    return {
        'theme': theme,
        'num_agents': num_agents,
        'form': form,
        'poem_length': poem_length,
        'length_unit': length_unit,
        'conversation_length': conversation_length,
        'use_openrouter': use_openrouter,
        'agent1_llm': llm1_choice,
        'agent2_llm': llm2_choice,
        'agent1_claude_model': claude1_model,
        'agent1_gemini_model': gemini1_model,
        'agent1_openai_model': openai1_model,
        'agent2_claude_model': claude2_model,
        'agent2_gemini_model': gemini2_model,
        'agent2_openai_model': openai2_model,
        'agent1_openrouter_search': agent1_openrouter_search,
        'agent2_openrouter_search': agent2_openrouter_search,
        'use_emojis': use_emojis,
        'output_format': 'markdown'  # Always use markdown output
    }

def validate_openrouter_model(model_id):
    """Validate an OpenRouter model and warn about potential issues.
    
    Args:
        model_id: The model ID to validate
        
    Returns:
        tuple: (is_valid, warnings, alternatives)
    """
    try:
        from openrouter_client import OpenRouterClient
        import os
        import requests
        
        # Check model availability directly without creating a client instance
        # This avoids the base class validation that causes the error
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            return False, ["❌ OPENROUTER_API_KEY not found"], []
        
        # Check if model exists in OpenRouter's model list
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        response.raise_for_status()
        models = response.json()["data"]
        
        # Find the specific model
        model_found = None
        for model in models:
            if model["id"] == model_id:
                model_found = model
                break
        
        if not model_found:
            return False, [f"❌ Model '{model_id}' not found in OpenRouter catalog"], []
        
        warnings = []
        alternatives = []
        
        # Check if it's a free model
        is_free_model = model_id.endswith(":free")
        if is_free_model:
            warnings.append("⚠️  This is a FREE model - may have upstream rate limits regardless of your credits")
            # Get paid alternatives without creating a client
            base_model = model_id.replace(":free", "")
            alternatives = [
                "anthropic/claude-3.5-sonnet",
                "openai/gpt-4o", 
                "meta-llama/llama-3.2-90b-vision-instruct"
            ]
            warnings.append(f"💡 Paid alternatives: {', '.join(alternatives[:3])}")
        
        return True, warnings, alternatives
        
    except Exception as e:
        return False, [f"❌ Error validating model: {str(e)}"], []

def ask_user_to_continue_or_choose_another(model_id, warnings, alternatives):
    """Ask user if they want to continue with a model that has warnings.
    
    Args:
        model_id: The model ID
        warnings: List of warning messages
        alternatives: List of alternative models
        
    Returns:
        tuple: (continue_with_model, new_model_id)
    """
    print(f"\n📋 Model Validation Results for {model_id}:")
    for warning in warnings:
        print(f"   {warning}")
    
    print("\nOptions:")
    print("1. Continue with this model anyway")
    print("2. Choose a different model")
    if alternatives:
        print("3. Use a recommended paid alternative")
    
    while True:
        choice = input("\nWhat would you like to do? (1/2/3): ").strip()
        
        if choice == "1":
            return True, model_id
        elif choice == "2":
            return False, None
        elif choice == "3" and alternatives:
            print("\nRecommended alternatives:")
            for i, alt in enumerate(alternatives[:5], 1):
                print(f"  {i}. {alt}")
            
            while True:
                try:
                    alt_choice = int(input(f"Select alternative (1-{len(alternatives[:5])}): ").strip())
                    if 1 <= alt_choice <= len(alternatives[:5]):
                        return True, alternatives[alt_choice - 1]
                    else:
                        print(f"Please enter a number between 1 and {len(alternatives[:5])}")
                except ValueError:
                    print("Please enter a valid number")
        else:
            print("Please enter '1', '2', or '3'")

def generate_title(theme):
    """Generate a title from the theme."""
    # Simple title generation - can be enhanced later
    words = theme.split()
    title = ' '.join(word.capitalize() for word in words)
    return title

def main():
    """Main function to run the poetry dialogue system."""
    try:
        # Get user input
        config = get_user_input()
        
        print(f"\n{'='*50}")
        print("Generating poetry dialogue...")
        print(f"{'='*50}")
        
        # Import and use dialogue manager
        from dialogue_manager import DialogueManager
        
        # Generate dialogue
        manager = DialogueManager()
        dialogue_data = manager.generate_dialogue(config)
        
        # Always save to markdown file
        filename = manager.save_dialogue_to_markdown(dialogue_data)
        print(f"\n✓ Poetry dialogue saved to: {filename}")
        
        # Open the file automatically if possible
        try:
            import subprocess
            import sys
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", filename])
            elif sys.platform == "win32":  # Windows
                subprocess.run(["start", filename], shell=True)
            elif sys.platform == "linux":  # Linux
                subprocess.run(["xdg-open", filename])
            print(f"✓ Opened {filename} in your default markdown viewer")
        except Exception:
            print(f"✓ File saved as {filename} - open it manually to view the formatted poetry")
        
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()