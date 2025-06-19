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
            return f"Write a haiku (5-7-5 syllables) about {theme}. Return only the 3-line haiku with no explanatory text. Put a blank line after the haiku."
        else:
            return f"Write {length} haiku stanzas about {theme}. Each stanza should be 3 lines following the 5-7-5 syllable pattern. Format as:\n\nFirst haiku (3 lines)\n\nSecond haiku (3 lines)\n\nReturn only the haiku verses with no explanatory text. Put a blank line after each individual haiku stanza."
    
    elif form == "prose":
        return f"Write a {length}-line prose poem about {theme}. Use free verse with natural language flow. Return only the poem with no explanatory text. Put a blank line after the poem."
    
    else:
        return f"Write a {form} poem of {length} lines about {theme}. Return only the poem with no explanatory text."

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
            base_prompt = f"You are {agent_name}. Respond to this poetry with a haiku (5-7-5 syllables). Incorporate elements, words, or themes from the previous poetry:\n\n{previous_poetry}\n\nReturn only the 3-line haiku with no explanatory text. Put a blank line after the haiku."
        else:
            base_prompt = f"You are {agent_name}. Respond to this poetry with {length} haiku stanzas. Each stanza should be 3 lines following the 5-7-5 syllable pattern. Incorporate elements, words, or themes from the previous poetry:\n\n{previous_poetry}\n\nFormat as:\n\nFirst haiku (3 lines)\n\nSecond haiku (3 lines)\n\nReturn only the haiku verses with no explanatory text. Put a blank line after each individual haiku stanza."
    
    elif form == "prose":
        base_prompt = f"You are {agent_name}. Respond to this poetry with a {length}-line prose poem. Use free verse and incorporate elements, words, or themes from the previous poetry:\n\n{previous_poetry}\n\nReturn only the poem with no explanatory text. Put a blank line after the poem."
    
    else:
        base_prompt = f"You are {agent_name}. Respond to this poetry with a {form} poem of {length} lines. Incorporate elements, words, or themes from the previous poetry:\n\n{previous_poetry}\n\nReturn only the poem with no explanatory text."
    
    return base_prompt

def create_title_prompt(theme: str) -> str:
    """
    Create a prompt to generate a title from the theme.
    
    Args:
        theme: The user-provided theme
        
    Returns:
        Formatted prompt for title generation
    """
    return f"Create a short, poetic title (2-4 words) based on this theme: {theme}. Return only the title with no explanatory text or punctuation."