"""
Prompt templates for poetry generation using Sonnet 4.
"""

def create_initial_poetry_prompt(theme: str, form: str, length: int) -> str:
    """
    Create a prompt for the first agent's poetry based on the theme.
    
    Args:
        theme: The user-provided theme
        form: Poetry form (haiku or prose)
        length: Length specification
        
    Returns:
        Formatted prompt for the LLM
    """
    if form == "haiku":
        if length == 1:
            return f"Create a haiku (5-7-5 syllables) about {theme}. Present it as a single 3-line haiku."
        else:
            return f"Create a haiku sequence of {length} stanzas about {theme}. Each stanza should be 3 lines following the 5-7-5 syllable pattern."
    
    elif form == "prose":
        return f"Create a {length}-line prose poem about {theme}. Use free verse with natural language flow."
    
    else:
        return f"Create a {form} poem of {length} lines about {theme}."

def create_response_poetry_prompt(agent_name: str, previous_poetry: str, form: str, length: int) -> str:
    """
    Create a prompt for an agent responding to previous poetry.
    
    Args:
        agent_name: Name of the responding agent
        previous_poetry: The poetry being responded to
        form: Poetry form (haiku or prose)
        length: Length specification
        
    Returns:
        Formatted prompt for the LLM
    """
    if form == "haiku":
        if length == 1:
            base_prompt = f"You are {agent_name}. Respond to this poetry with a haiku (5-7-5 syllables). Incorporate elements, words, or themes from the previous poetry:\n\n{previous_poetry}\n\nYour response as a single 3-line haiku:"
        else:
            base_prompt = f"You are {agent_name}. Respond to this poetry with a haiku sequence of {length} stanzas. Each stanza should be 3 lines following the 5-7-5 syllable pattern. Incorporate elements, words, or themes from the previous poetry:\n\n{previous_poetry}\n\nYour response:"
    
    elif form == "prose":
        base_prompt = f"You are {agent_name}. Respond to this poetry with a {length}-line prose poem. Use free verse and incorporate elements, words, or themes from the previous poetry:\n\n{previous_poetry}\n\nYour response:"
    
    else:
        base_prompt = f"You are {agent_name}. Respond to this poetry with a {form} poem of {length} lines. Incorporate elements, words, or themes from the previous poetry:\n\n{previous_poetry}\n\nYour response:"
    
    return base_prompt

def create_title_prompt(theme: str) -> str:
    """
    Create a prompt to generate a title from the theme.
    
    Args:
        theme: The user-provided theme
        
    Returns:
        Formatted prompt for title generation
    """
    return f"Create a short, poetic title (2-4 words) based on this theme: {theme}. Return only the title, nothing else."