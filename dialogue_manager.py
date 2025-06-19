"""
Dialogue Manager for orchestrating poetry agent conversations.
"""

from typing import List, Dict, Any
from llm_client import LLMClient
from prompts import create_initial_poetry_prompt, create_response_poetry_prompt, create_title_prompt
from character_names import get_random_names

class DialogueManager:
    """Manages the poetry dialogue between agents."""
    
    def __init__(self):
        """Initialize the dialogue manager."""
        self.llm_client = LLMClient()
        self.agents = []
        self.conversation_history = []
    
    def generate_dialogue(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a complete poetry dialogue based on configuration.
        
        Args:
            config: Dictionary containing theme, num_agents, form, poem_length, conversation_length
            
        Returns:
            Dictionary containing title, agents, and dialogue history
        """
        # Generate title from theme
        title_prompt = create_title_prompt(config['theme'])
        title = self.llm_client.generate_poetry(title_prompt, max_tokens=20)
        
        # Get agent names
        agent_names = get_random_names(config['num_agents'])
        self.agents = agent_names
        
        # Initialize conversation history
        self.conversation_history = []
        
        # Generate the dialogue
        for round_num in range(config['conversation_length']):
            for agent_index in range(config['num_agents']):
                agent_name = agent_names[agent_index]
                
                if round_num == 0 and agent_index == 0:
                    # First agent creates poetry from theme
                    prompt = create_initial_poetry_prompt(
                        config['theme'], 
                        config['form'], 
                        config['poem_length']
                    )
                else:
                    # Subsequent agents respond to previous poetry
                    previous_poetry = self.conversation_history[-1]['poetry']
                    prompt = create_response_poetry_prompt(
                        agent_name,
                        previous_poetry,
                        config['form'],
                        config['poem_length']
                    )
                
                # Generate poetry
                poetry = self.llm_client.generate_poetry(prompt, max_tokens=300)
                
                # Add to conversation history
                self.conversation_history.append({
                    'agent': agent_name,
                    'poetry': poetry,
                    'round': round_num + 1,
                    'agent_index': agent_index
                })
        
        return {
            'title': title,
            'agents': agent_names,
            'conversation': self.conversation_history,
            'config': config
        }
    
    def format_dialogue_output(self, dialogue_data: Dict[str, Any]) -> str:
        """
        Format the dialogue for display.
        
        Args:
            dialogue_data: Output from generate_dialogue
            
        Returns:
            Formatted string for display
        """
        output = []
        
        # Title (in larger bold font - using markdown)
        output.append(f"# {dialogue_data['title']}")
        output.append("")
        
        # Display each agent's poetry
        for entry in dialogue_data['conversation']:
            # Agent name in bold
            output.append(f"**{entry['agent']}:**")
            output.append("")
            
            # Poetry (indented for readability)
            poetry_lines = entry['poetry'].split('\n')
            for line in poetry_lines:
                if line.strip():  # Skip empty lines
                    output.append(line)
            
            output.append("")  # Empty line between agents
        
        return '\n'.join(output)