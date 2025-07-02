#!/usr/bin/env python3
"""
Poetry Agent Dialogue System
Main entry point for the poetry dialogue generator.
"""

def get_user_input():
    """Collect the 7 required questions from the user."""
    print("Welcome to Poetry Agent Dialogue Generator!")
    print("Please answer the following questions:\n")
    
    # Question 1: Theme
    theme = input("1. What is the theme? ")
    
    # Always use 2 agents
    num_agents = 2
    
    # Question 2: Form of dialogue
    valid_forms = ['haiku', 'prose', 'sonnet', 'villanelle', 'limerick', 'ballad', 'ghazal', 'tanka']
    while True:
        print("Available forms: haiku, prose, sonnet, villanelle, limerick, ballad, ghazal, tanka")
        form = input("2. What is the form of dialogue? ").lower().strip()
        if form in valid_forms:
            break
        else:
            print(f"Please enter one of: {', '.join(valid_forms)}")
    
    # Question 3: Length of each poem (form-dependent)
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
        print(f"3. Poem length: {poem_length} {length_unit} (traditional {form})")
    else:
        # Variable forms need user input
        if form == 'ballad':
            while True:
                try:
                    poem_length = int(input("3. How many stanzas for each ballad? "))
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
                    poem_length = int(input("3. How many couplets for each ghazal? (5-15 recommended) "))
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
                    poem_length = int(input("3. How many paragraphs for each prose piece? "))
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
                    poem_length = int(input("3. What is the length of each poem? "))
                    if poem_length > 0:
                        length_unit = 'lines'
                        break
                    else:
                        print("Please enter a positive number.")
                except ValueError:
                    print("Please enter a valid number.")
    
    # Question 4: Length of conversation (clarified as rounds)
    while True:
        try:
            conversation_length = int(input("4. How many rounds of conversation? (each agent will write one poem per round) "))
            if conversation_length > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Question 5: LLM for Agent 1
    while True:
        llm1_choice = input("5. Which LLM should Agent 1 use? (Claude/Gemini) ").strip().title()
        if llm1_choice in ['Claude', 'Gemini']:
            break
        else:
            print("Please enter 'Claude' or 'Gemini'.")
    
    # Question 6: LLM for Agent 2 (always ask since we always have 2 agents)
    while True:
        llm2_choice = input("6. Which LLM should Agent 2 use? (Claude/Gemini) ").strip().title()
        if llm2_choice in ['Claude', 'Gemini']:
            break
        else:
            print("Please enter 'Claude' or 'Gemini'.")
    
    # Question 7: Emoji preference
    while True:
        emoji_choice = input("7. Add emojis to enhance the poetry? (yes/no) ").lower().strip()
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
        'agent1_llm': llm1_choice,
        'agent2_llm': llm2_choice,
        'use_emojis': use_emojis,
        'output_format': 'markdown'  # Always use markdown output
    }

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