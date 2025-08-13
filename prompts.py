"""
Prompt templates for poetry generation using Sonnet 4.
"""

from character_names import get_character_persona, get_enhanced_character_persona
from poetry_rules import get_poetry_rules, get_formatting_rules, get_quality_guidelines

def create_initial_poetry_prompt(theme: str, form: str, length: int, agent_name: str = None) -> str:
    """
    Create a prompt for the first agent's poetry based on the theme.
    
    Args:
        theme: The user-provided theme
        form: Poetry form (haiku, prose, sonnet, villanelle, limerick, ballad, ghazal, tanka)
        length: Length specification
        agent_name: Optional agent name for persona (if None, uses generic prompt)
        
    Returns:
        Formatted prompt for the LLM with comprehensive structural rules
    """
    # Get enhanced persona if agent name is provided
    persona_prefix = ""
    if agent_name:
        persona = get_enhanced_character_persona(agent_name)
        persona_prefix = f"{persona}\n\n"
    
    # Get comprehensive rules for the poetry form
    structural_rules = get_poetry_rules(form)
    formatting_rules = get_formatting_rules()
    quality_guidelines = get_quality_guidelines()
    
    # Handle length variations for specific forms
    length_instruction = ""
    if form == "haiku" and length > 1:
        length_instruction = f"\n\nWrite {length} haiku about the theme. Put a blank line between each haiku."
    elif form == "limerick" and length > 1:
        length_instruction = f"\n\nWrite {length} limericks about the theme. Put a blank line between each limerick."
    elif form == "tanka" and length > 1:
        length_instruction = f"\n\nWrite {length} tanka about the theme. Put a blank line between each tanka."
    elif form == "ballad":
        length_instruction = f"\n\nWrite a ballad with {length} stanzas about the theme."
    elif form == "ghazal":
        length_instruction = f"\n\nWrite a ghazal with {length} couplets about the theme."
    elif form == "prose":
        length_instruction = f"\n\nWrite a prose poem with {length} paragraphs about the theme."
    
    # Construct the comprehensive prompt
    prompt = f"""{persona_prefix}TASK: Write a {form} about the theme: "{theme}"{length_instruction}

{structural_rules}

{quality_guidelines}

{formatting_rules}

THEME: {theme}

Begin writing your {form} now:"""
    
    return prompt

def create_response_poetry_prompt(agent_name: str, conversation_context: str, form: str, length: int) -> str:
    """
    Create a prompt for an agent responding to the complete conversation history.
    
    Args:
        agent_name: Name of the responding agent
        conversation_context: The complete conversation context including theme and all previous poems
        form: Poetry form (haiku, prose, sonnet, villanelle, limerick, ballad, ghazal, tanka)
        length: Length specification
        
    Returns:
        Formatted prompt for the LLM with comprehensive structural rules
    """
    # Get the character's enhanced literary persona
    persona = get_enhanced_character_persona(agent_name)
    
    # Get comprehensive rules for the poetry form
    structural_rules = get_poetry_rules(form)
    formatting_rules = get_formatting_rules()
    quality_guidelines = get_quality_guidelines()
    
    # Handle length variations for specific forms
    length_instruction = ""
    if form == "haiku" and length > 1:
        length_instruction = f"\n\nRespond with {length} haiku. Put a blank line between each haiku."
    elif form == "limerick" and length > 1:
        length_instruction = f"\n\nRespond with {length} limericks. Put a blank line between each limerick."
    elif form == "tanka" and length > 1:
        length_instruction = f"\n\nRespond with {length} tanka. Put a blank line between each tanka."
    elif form == "ballad":
        length_instruction = f"\n\nRespond with a ballad of {length} stanzas."
    elif form == "ghazal":
        length_instruction = f"\n\nRespond with a ghazal of {length} couplets."
    elif form == "prose":
        length_instruction = f"\n\nRespond with a prose poem of {length} paragraphs."
    
    # Construct the comprehensive response prompt
    prompt = f"""{persona}

TASK: Respond to this poetic dialogue with a {form}.{length_instruction}

DIALOGUE RESPONSE REQUIREMENTS:
• CRITICAL: Your poem MUST include at least ONE specific word, image, or concept from the immediately preceding poem
• Transform or reinterpret that element through your character's unique perspective
• FORBIDDEN: Writing poems that could exist independently of this conversation
• REQUIRED: Poems that clearly build upon, challenge, or transform what came before

RESPONSE PROCESS:
1. Identify the strongest image/metaphor from the previous poem
2. Consider how your character would interpret or respond to that image  
3. Build your poem around that connection while maintaining your distinctive voice

DIALOGUE TEST: A reader should be able to identify which specific element from the previous poem you're responding to. If the connection isn't clear, you must revise.

CHARACTER PERSPECTIVE: As {agent_name}, interpret the previous speaker's central image through your unique worldview. How does their metaphor relate to your experiences, conflicts, or philosophy?

{structural_rules}

{quality_guidelines}

{formatting_rules}

CONVERSATION HISTORY:
{conversation_context}

Respond with your {form} now:"""
    
    return prompt

def create_title_prompt(theme: str) -> str:
    """
    Create a prompt to generate a title from the theme.
    
    Args:
        theme: The user-provided theme
        
    Returns:
        Formatted prompt for title generation
    """
    return f"Create a short, poetic title (2-4 words) based on this theme: {theme}. Return only the title with no explanatory text or punctuation."