"""
Dialogue Manager for orchestrating poetry agent conversations.
"""

import os
from typing import List, Dict, Any
from llm_client import LLMClient
from gemini_client import GeminiClient
from prompts import create_initial_poetry_prompt, create_response_poetry_prompt, create_title_prompt
from character_names import get_random_names, get_character_info

class DialogueManager:
    """Manages the poetry dialogue between agents."""
    
    def __init__(self):
        """Initialize the dialogue manager."""
        self.claude_client = LLMClient()
        self.gemini_client = GeminiClient()
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
        # Generate title from theme using Claude
        title_prompt = create_title_prompt(config['theme'])
        title = self.claude_client.generate_poetry(title_prompt, max_tokens=20)
        
        # Generate ASCII art for the theme
        ascii_art = self.generate_ascii_art(config['theme'])
        
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
                    # Subsequent agents respond to previous poetry
                    previous_poetry = self.conversation_history[-1]['poetry']
                    prompt = create_response_poetry_prompt(
                        agent_name,
                        previous_poetry,
                        config['form'],
                        config['poem_length']
                    )
                
                # Use user-specified LLM for each agent
                if agent_index == 0:
                    # First agent uses user-selected LLM
                    if config.get('agent1_llm', 'Claude') == 'Claude':
                        poetry = self.claude_client.generate_poetry(prompt, max_tokens=300)
                        llm_used = "Claude"
                    else:
                        poetry = self.gemini_client.generate_poetry(prompt, max_tokens=300)
                        llm_used = "Gemini"
                else:
                    # Second agent uses user-selected LLM
                    if config.get('agent2_llm', 'Gemini') == 'Claude':
                        poetry = self.claude_client.generate_poetry(prompt, max_tokens=300)
                        llm_used = "Claude"
                    else:
                        poetry = self.gemini_client.generate_poetry(prompt, max_tokens=300)
                        llm_used = "Gemini"
                
                # Add emojis if requested
                if config.get('use_emojis', False):
                    poetry = self.add_emojis_to_poetry(poetry, config['theme'])
                
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
    
    def generate_ascii_art(self, theme: str) -> str:
        """
        Generate ASCII art based on the theme using LLM.
        
        Args:
            theme: The theme to create ASCII art for
            
        Returns:
            ASCII art as a string
        """
        ascii_prompt = f"""Create simple ASCII art (text art) that represents the poetic theme: "{theme}". 

Guidelines:
- Use only basic ASCII characters: - | / \\ * + = ~ ^ v < > . : ; ' " ( ) [ ] {{ }} @ # $ % & 
- Keep it small but impactful (4-8 lines maximum)
- Make it visually appealing and thematically appropriate
- Consider the poetic and artistic nature of the theme
- Create something that would complement poetry about this theme

Examples of good ASCII art themes:
- Snow/winter: snowflakes, bare trees, mountains
- Ocean/water: waves, boats, fish
- Night/stars: moon, stars, constellation patterns  
- Love/romance: hearts, flowers, intertwined elements
- Archery: bows, arrows, targets
- Games: board patterns, pieces
- Nature: trees, animals, landscapes

Return ONLY the ASCII art with no explanatory text or comments."""
        
        ascii_art = self.claude_client.generate_poetry(ascii_prompt, max_tokens=250)
        return ascii_art.strip()
    
    def add_emojis_to_poetry(self, poetry: str, theme: str) -> str:
        """
        Add emojis to poetry by enhancing words with relevant emojis.
        
        Args:
            poetry: The original poetry text
            theme: The theme to help context for emoji selection
            
        Returns:
            Poetry enhanced with emojis placed after relevant words
        """
        emoji_prompt = f"""Add emojis to enhance this poetry about "{theme}". 

Instructions:
- Place emojis immediately AFTER words they represent (word🌟 not 🌟word)
- Only add emojis to nouns, nature words, emotions, and vivid imagery words
- Don't add emojis to articles, prepositions, or common words like "the", "and", "in"
- Use 2-4 emojis per line maximum to avoid overwhelming the poetry
- Choose emojis that enhance the poetic imagery and theme
- Preserve the exact line structure and spacing of the original
- Return ONLY the enhanced poetry with no explanatory text or comments

Original poetry:
{poetry}

Return the poetry with emojis added, maintaining the same line breaks and structure."""
        
        enhanced_poetry = self.claude_client.generate_poetry(emoji_prompt, max_tokens=400)
        return enhanced_poetry.strip()
    
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