#!/usr/bin/env python3
"""
Poetry Agent Dialogue System
Main entry point for the poetry dialogue generator.
"""

def get_user_input():
    """Collect the 5 required questions from the user."""
    print("Welcome to Poetry Agent Dialogue Generator!")
    print("Please answer the following questions:\n")
    
    # Question 1: Theme
    theme = input("1. What is the theme? ")
    
    # Question 2: Number of agents
    while True:
        try:
            num_agents = int(input("2. How many agents are there? "))
            if num_agents > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Question 3: Form of dialogue
    while True:
        form = input("3. What is the form of dialogue? (haiku/prose) ").lower().strip()
        if form in ['haiku', 'prose']:
            break
        else:
            print("Please enter 'haiku' or 'prose'.")
    
    # Question 4: Length of each poem
    while True:
        try:
            poem_length = int(input("4. What is the length of each poem? "))
            if poem_length > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Question 5: Length of conversation
    while True:
        try:
            conversation_length = int(input("5. What is the length of the conversation? "))
            if conversation_length > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    return {
        'theme': theme,
        'num_agents': num_agents,
        'form': form,
        'poem_length': poem_length,
        'conversation_length': conversation_length
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
        
        # Display formatted output
        formatted_output = manager.format_dialogue_output(dialogue_data)
        print("\n" + formatted_output)
        
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()