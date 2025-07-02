"""
Prompt templates for poetry generation using Sonnet 4.
"""

from character_names import get_character_persona

def create_initial_poetry_prompt(theme: str, form: str, length: int, agent_name: str = None) -> str:
    """
    Create a prompt for the first agent's poetry based on the theme.
    
    Args:
        theme: The user-provided theme
        form: Poetry form (haiku, prose, sonnet, villanelle, limerick, ballad, ghazal, tanka)
        length: Length specification
        agent_name: Optional agent name for persona (if None, uses generic prompt)
        
    Returns:
        Formatted prompt for the LLM
    """
    # Get persona if agent name is provided
    persona_prefix = ""
    if agent_name:
        persona = get_character_persona(agent_name)
        persona_prefix = f"{persona} "
    
    if form == "haiku":
        if length == 1:
            return f"{persona_prefix}Write a haiku (5-7-5 syllables) about {theme}. Return only the 3-line haiku with no explanatory text. Put a blank line after the haiku."
        else:
            return f"{persona_prefix}Write {length} haiku stanzas about {theme}. Each stanza should be 3 lines following the 5-7-5 syllable pattern. Format as:\n\nFirst haiku (3 lines)\n\nSecond haiku (3 lines)\n\nReturn only the haiku verses with no explanatory text. Put a blank line after each individual haiku stanza."
    
    elif form == "prose":
        return f"{persona_prefix}Write a {length}-line prose poem about {theme}. Use free verse with natural language flow. Return only the poem with no explanatory text. Put a blank line after the poem."
    
    elif form == "sonnet":
        return f"{persona_prefix}Write a Shakespearean sonnet about {theme}. Follow the ABAB CDCD EFEF GG rhyme scheme with 14 lines of iambic pentameter. End with a rhyming couplet that provides resolution or insight. Return only the sonnet with no explanatory text."
    
    elif form == "villanelle":
        return f"{persona_prefix}Write a villanelle about {theme}. Use the traditional form: 19 lines with two refrains and two rhymes, with the first and third line of the opening tercet repeated alternately until the last stanza, which includes both refrains. Pattern: A1bA2 abA1 abA2 abA1 abA2 abA1A2. Return only the villanelle with no explanatory text."
    
    elif form == "limerick":
        if length == 1:
            return f"{persona_prefix}Write a limerick about {theme}. Follow the AABBA rhyme scheme with 5 lines in anapestic meter. Make it witty and playful. Return only the limerick with no explanatory text."
        else:
            return f"{persona_prefix}Write {length} limericks about {theme}. Each should follow the AABBA rhyme scheme with 5 lines in anapestic meter. Make them witty and playful. Put a blank line between each limerick. Return only the limericks with no explanatory text."
    
    elif form == "ballad":
        return f"{persona_prefix}Write a ballad about {theme}. Use quatrains (4-line stanzas) with ABAB or ABCB rhyme scheme, typically in iambic meter. Tell a story with narrative progression. Write {length} stanzas. Return only the ballad with no explanatory text."
    
    elif form == "ghazal":
        return f"{persona_prefix}Write a ghazal about {theme}. Use 5-15 couplets where each couplet is independent but connected thematically. The second line of each couplet should end with the same word or phrase (radif). Focus on themes of love, loss, or longing. Return only the ghazal with no explanatory text."
    
    elif form == "tanka":
        if length == 1:
            return f"{persona_prefix}Write a tanka about {theme}. Follow the 5-7-5-7-7 syllable pattern across 5 lines. Often includes a pivot between lines 2-3 or 3-4. Return only the tanka with no explanatory text."
        else:
            return f"{persona_prefix}Write {length} tanka about {theme}. Each should follow the 5-7-5-7-7 syllable pattern across 5 lines. Put a blank line between each tanka. Return only the tanka with no explanatory text."
    
    else:
        return f"{persona_prefix}Write a {form} poem about {theme}. Return only the poem with no explanatory text."

def create_response_poetry_prompt(agent_name: str, previous_poetry: str, form: str, length: int) -> str:
    """
    Create a prompt for an agent responding to previous poetry.
    
    Args:
        agent_name: Name of the responding agent
        previous_poetry: The poetry being responded to
        form: Poetry form (haiku, prose, sonnet, villanelle, limerick, ballad, ghazal, tanka)
        length: Length specification
        
    Returns:
        Formatted prompt for the LLM
    """
    # Get the character's literary persona
    persona = get_character_persona(agent_name)
    
    if form == "haiku":
        if length == 1:
            base_prompt = f"{persona} Respond to this poetry with a haiku (5-7-5 syllables). Incorporate elements, words, or themes from the previous poetry while expressing your distinctive character voice:\n\n{previous_poetry}\n\nReturn only the 3-line haiku with no explanatory text. Put a blank line after the haiku."
        else:
            base_prompt = f"{persona} Respond to this poetry with {length} haiku stanzas. Each stanza should be 3 lines following the 5-7-5 syllable pattern. Incorporate elements, words, or themes from the previous poetry while expressing your distinctive character voice:\n\n{previous_poetry}\n\nFormat as:\n\nFirst haiku (3 lines)\n\nSecond haiku (3 lines)\n\nReturn only the haiku verses with no explanatory text. Put a blank line after each individual haiku stanza."
    
    elif form == "prose":
        base_prompt = f"{persona} Respond to this poetry with a {length}-line prose poem. Use free verse and incorporate elements, words, or themes from the previous poetry while expressing your distinctive character voice:\n\n{previous_poetry}\n\nReturn only the poem with no explanatory text. Put a blank line after the poem."
    
    elif form == "sonnet":
        base_prompt = f"{persona} Respond to this poetry with a Shakespearean sonnet. Follow the ABAB CDCD EFEF GG rhyme scheme with 14 lines of iambic pentameter. Incorporate elements, words, or themes from the previous poetry while expressing your distinctive character voice:\n\n{previous_poetry}\n\nReturn only the sonnet with no explanatory text."
    
    elif form == "villanelle":
        base_prompt = f"{persona} Respond to this poetry with a villanelle. Use the traditional 19-line form with two refrains and two rhymes. Incorporate elements, words, or themes from the previous poetry while expressing your distinctive character voice:\n\n{previous_poetry}\n\nReturn only the villanelle with no explanatory text."
    
    elif form == "limerick":
        if length == 1:
            base_prompt = f"{persona} Respond to this poetry with a limerick. Follow the AABBA rhyme scheme with 5 lines in anapestic meter. Make it witty and incorporate elements from the previous poetry while expressing your distinctive character voice:\n\n{previous_poetry}\n\nReturn only the limerick with no explanatory text."
        else:
            base_prompt = f"{persona} Respond to this poetry with {length} limericks. Each should follow the AABBA rhyme scheme. Make them witty and incorporate elements from the previous poetry while expressing your distinctive character voice:\n\n{previous_poetry}\n\nReturn only the limericks with no explanatory text."
    
    elif form == "ballad":
        base_prompt = f"{persona} Respond to this poetry with a ballad of {length} stanzas. Use quatrains with ABAB or ABCB rhyme scheme and tell a story. Incorporate elements, words, or themes from the previous poetry while expressing your distinctive character voice:\n\n{previous_poetry}\n\nReturn only the ballad with no explanatory text."
    
    elif form == "ghazal":
        base_prompt = f"{persona} Respond to this poetry with a ghazal. Use 5-15 couplets with the same radif (ending phrase). Focus on themes of love, loss, or longing. Incorporate elements from the previous poetry while expressing your distinctive character voice:\n\n{previous_poetry}\n\nReturn only the ghazal with no explanatory text."
    
    elif form == "tanka":
        if length == 1:
            base_prompt = f"{persona} Respond to this poetry with a tanka. Follow the 5-7-5-7-7 syllable pattern across 5 lines. Incorporate elements from the previous poetry while expressing your distinctive character voice:\n\n{previous_poetry}\n\nReturn only the tanka with no explanatory text."
        else:
            base_prompt = f"{persona} Respond to this poetry with {length} tanka. Each should follow the 5-7-5-7-7 syllable pattern. Incorporate elements from the previous poetry while expressing your distinctive character voice:\n\n{previous_poetry}\n\nReturn only the tanka with no explanatory text."
    
    else:
        base_prompt = f"{persona} Respond to this poetry with a {form} poem. Incorporate elements, words, or themes from the previous poetry while expressing your distinctive character voice:\n\n{previous_poetry}\n\nReturn only the poem with no explanatory text."
    
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