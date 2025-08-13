"""
Dialogue Manager for orchestrating poetry agent conversations.
Refactored to use factory pattern and extracted services.
"""

import os
import datetime
import re
from typing import List, Dict, Any
from llm_factory import LLMClientFactory
from enhancement_service import EnhancementService
from llm_client import LLMClient
from prompts import create_initial_poetry_prompt, create_response_poetry_prompt, create_title_prompt
from character_names import get_random_names, get_character_info
from exceptions import ConfigurationError, APIError

class DialogueManager:
    """Manages the poetry dialogue between agents."""
    
    def __init__(self):
        """Initialize the dialogue manager."""
        self.agents = []
        self.conversation_history = []
        self.enhancement_service = EnhancementService()
    
    def generate_dialogue(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a complete poetry dialogue based on configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Dictionary containing title, agents, and dialogue history
        """
        # Validate configuration
        LLMClientFactory.validate_configuration(config)
        
        # Generate title using default Claude client
        title = self._generate_title(config['theme'])
        
        # Generate ASCII art for the theme
        ascii_art = self.enhancement_service.generate_ascii_art(config['theme'])
        
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
                        config['poem_length'],
                        agent_name
                    )
                else:
                    # Subsequent agents respond to complete conversation history
                    conversation_context = self._build_conversation_context(
                        config['theme'], 
                        self.conversation_history
                    )
                    prompt = create_response_poetry_prompt(
                        agent_name,
                        conversation_context,
                        config['form'],
                        config['poem_length']
                    )
                
                # Create client for this agent using factory
                client = LLMClientFactory.create_client(config, agent_index + 1)
                llm_used = LLMClientFactory.get_client_display_name(config, agent_index + 1)
                
                # Generate poetry
                poetry = client.generate_poetry(prompt, max_tokens=300)
                
                # Add emojis if requested
                if config.get('use_emojis', False):
                    poetry = self.enhancement_service.add_emojis_to_poetry(poetry, config['theme'])
                
                # Add to conversation history
                self.conversation_history.append({
                    'agent': agent_name,
                    'poetry': poetry,
                    'round': round_num + 1,
                    'agent_index': agent_index,
                    'llm_used': llm_used
                })
        
        return {
            'title': title,
            'ascii_art': ascii_art,
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
    
    def _generate_title(self, theme: str) -> str:
        """Generate title from theme using default Claude client."""
        try:
            title_client = LLMClient()  # Use default Claude
            title_prompt = create_title_prompt(theme)
            return title_client.generate_poetry(title_prompt, max_tokens=20)
        except Exception:
            # Fallback title generation
            words = theme.split()
            return ' '.join(word.capitalize() for word in words[:3])
    
    
    def save_dialogue_to_markdown(self, dialogue_data: Dict[str, Any], filename: str = None) -> str:
        """
        Save the dialogue to a markdown file with enhanced formatting.
        
        Args:
            dialogue_data: Output from generate_dialogue
            filename: Optional filename (if None, generates from title and timestamp)
            
        Returns:
            The filename of the saved file
        """
        import datetime
        import re
        
        if not filename:
            # Create filename from title and timestamp
            title_clean = re.sub(r'[^\w\s-]', '', dialogue_data['title']).strip()
            title_clean = re.sub(r'[-\s]+', '_', title_clean).lower()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"outputs/poetry_dialogue_{title_clean}_{timestamp}.md"
            
            # Ensure outputs directory exists
            os.makedirs('outputs', exist_ok=True)
        
        # Create enhanced markdown content
        content = []
        
        # Title with date
        content.append(f"# {dialogue_data['title']}")
        content.append(f"*Generated on {datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p')}*")
        content.append("")
        
        # ASCII art in code block for proper formatting
        if 'ascii_art' in dialogue_data and dialogue_data['ascii_art']:
            content.append("```")
            content.append(dialogue_data['ascii_art'])
            content.append("```")
            content.append("")
        
        # Configuration details
        config = dialogue_data['config']
        content.append("## Dialogue Configuration")
        content.append(f"- **Theme:** {config['theme']}")
        content.append(f"- **Agents:** {config['num_agents']} ({', '.join(dialogue_data['agents'])})")
        content.append(f"- **Form:** {config['form'].title()}")
        # Use the length_unit from config to create appropriate description
        length_unit = config.get('length_unit', 'lines')
        poem_length = config['poem_length']
        
        if length_unit == 'lines':
            if config['form'] in ['haiku', 'sonnet', 'villanelle', 'limerick', 'tanka']:
                length_desc = f"{poem_length} {length_unit} (traditional {config['form']})"
            else:
                length_desc = f"{poem_length} {length_unit}"
        elif length_unit == 'stanzas':
            length_desc = f"{poem_length} {'stanza' if poem_length == 1 else 'stanzas'}"
        elif length_unit == 'couplets':
            length_desc = f"{poem_length} {'couplet' if poem_length == 1 else 'couplets'}"
        elif length_unit == 'paragraphs':
            length_desc = f"{poem_length} {'paragraph' if poem_length == 1 else 'paragraphs'}"
        else:
            length_desc = f"{poem_length} {length_unit}"
        
        content.append(f"- **Poem Length:** {length_desc}")
        content.append(f"- **Conversation Length:** {config['conversation_length']} rounds")
        content.append(f"- **Emojis:** {'Enabled' if config.get('use_emojis', False) else 'Disabled'}")
        content.append("")
        
        # Agent details
        content.append("## Literary Agents")
        content.append("")
        for agent_name in dialogue_data['agents']:
            char_info = get_character_info(agent_name)
            content.append(f"### {agent_name}")
            content.append(f"**Source:** {char_info['source']}")
            content.append("")
            content.append(f"**Character Qualities:** {char_info['qualities']}")
            content.append("")
        
        content.append("---")
        content.append("")
        
        # Poetry dialogue with enhanced formatting
        for entry in dialogue_data['conversation']:
            # Agent name as section header with LLM indicator
            llm_indicator = entry.get('llm_used', 'Unknown')
            content.append(f"## {entry['agent']} *(via {llm_indicator})*")
            content.append("")
            
            # Poetry without quote blocks for cleaner appearance
            poetry_lines = entry['poetry'].split('\n')
            for line in poetry_lines:
                if line.strip():
                    content.append(line)
                else:
                    content.append("")
            content.append("")
            content.append("---")
            content.append("")
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        return filename
    
    def _build_conversation_context(self, theme: str, conversation_history: List[Dict[str, Any]]) -> str:
        """
        Build the complete conversation context including theme and all previous poems.
        
        Args:
            theme: The original theme that started the conversation
            conversation_history: List of conversation entries so far
            
        Returns:
            Formatted string containing the complete conversation context
        """
        context_parts = []
        
        # Start with the original theme
        context_parts.append(f"Theme: {theme}")
        context_parts.append("")
        
        # Add each poem in the conversation so far
        for entry in conversation_history:
            context_parts.append(f"{entry['agent']}:")
            context_parts.append(entry['poetry'])
            context_parts.append("")
        
        return "\n".join(context_parts)
    
