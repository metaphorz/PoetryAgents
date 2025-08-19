"""
Critique Service for automated poetry conversation evaluation and improvement.
Uses a third-party LLM judge-editor to critique and enhance poetry dialogues.
"""

import re
from typing import Dict, Any, List, Tuple
from llm_client import LLMClient
from gemini_client import GeminiClient
from openai_client import OpenAIClient
from openrouter_client import OpenRouterClient
from turner_rules import TurnerRulesManager


class CritiqueService:
    """Service for critiquing and improving poetry conversations using a judge-editor LLM."""
    
    # No hardcoded models - use dynamic latest model selection
    
    def __init__(self):
        """Initialize the critique service."""
        self.turner_rules = TurnerRulesManager()
    
    def select_judge(self, config: Dict[str, Any]) -> Tuple[str, Any]:
        """
        Select the judge-editor LLM based on which companies/providers are NOT used in the conversation.
        Ensures judge-editor uses a different company than any agent.
        
        Args:
            config: Configuration dictionary containing agent LLM choices
            
        Returns:
            Tuple of (company_name, judge_editor_client_instance)
        """
        # Company mapping for proper identification
        COMPANY_MAPPING = {
            'Claude': 'Anthropic',
            'Anthropic': 'Anthropic', 
            'Gemini': 'Google',
            'OpenAI': 'OpenAI'
        }
        
        # Track which companies are used and which specific models
        used_companies = set()
        used_models = set()
        
        # Check if using OpenRouter
        if config.get('use_openrouter', False):
            # For OpenRouter, analyze which models are being used to determine companies
            for i in range(config.get('num_agents', 2)):
                agent_key = f'agent{i+1}_openrouter_search'
                if agent_key in config:
                    model_id = config[agent_key]
                    used_models.add(model_id)
                    
                    # Determine company from OpenRouter model ID
                    if model_id.startswith('anthropic/'):
                        used_companies.add('Anthropic')
                    elif model_id.startswith('google/') or model_id.startswith('google-'):
                        used_companies.add('Google')
                    elif model_id.startswith('openai/'):
                        used_companies.add('OpenAI')
            
            # Select judge-editor from unused company through OpenRouter
            judge_editor_client = self._create_openrouter_judge_editor(used_companies, used_models)
            return 'OpenRouter', judge_editor_client
        else:
            # Check direct API usage
            for i in range(config.get('num_agents', 2)):
                agent_key = f'agent{i+1}_llm'
                model_key = None
                
                if agent_key in config:
                    llm_choice = config[agent_key]
                    company = COMPANY_MAPPING.get(llm_choice, llm_choice)
                    used_companies.add(company)
                    
                    # Get the specific model being used
                    if llm_choice in ['Claude', 'Anthropic']:
                        model_key = f'agent{i+1}_claude_model'
                    elif llm_choice == 'Gemini':
                        model_key = f'agent{i+1}_gemini_model'
                    elif llm_choice == 'OpenAI':
                        model_key = f'agent{i+1}_openai_model'
                    
                    if model_key and model_key in config:
                        used_models.add(config[model_key])
        
        # Select judge-editor from unused company - prioritize Google > Anthropic > OpenAI for latest models
        available_companies = ['Google', 'Anthropic', 'OpenAI']
        
        for company in available_companies:
            if company not in used_companies:
                judge_editor_client = self._create_judge_editor_client_by_company(company, used_models)
                return company, judge_editor_client
        
        # If all companies are used (shouldn't happen with 2 agents), raise an error
        raise ValueError("Cannot select judge-editor: all companies are already used in conversation")
    
    def _create_judge_editor_client_by_company(self, company: str, used_models: set) -> Any:
        """
        Create a judge-editor client for the specified company, avoiding used models.
        
        Args:
            company: Company name ('Google', 'Anthropic', 'OpenAI')
            used_models: Set of model names/IDs already used by agents
            
        Returns:
            Initialized client instance
        """
        if company == 'Google':
            from gemini_client import GeminiClient
            available_models = GeminiClient.get_available_models()
            # Find a model not used by agents
            for display_name, model_id in available_models.items():
                if display_name not in used_models and model_id not in used_models:
                    return GeminiClient(display_name)
            # If all models used, use the latest one anyway
            latest_model = list(available_models.keys())[0]
            return GeminiClient(latest_model)
            
        elif company == 'Anthropic':
            from llm_client import LLMClient
            available_models = LLMClient.get_available_models()
            # Find a model not used by agents
            for display_name, model_id in available_models.items():
                if display_name not in used_models and model_id not in used_models:
                    return LLMClient(display_name)
            # If all models used, use the latest one anyway
            latest_model = list(available_models.keys())[0]
            return LLMClient(latest_model)
            
        elif company == 'OpenAI':
            from openai_client import OpenAIClient
            available_models = OpenAIClient.get_available_models()
            # Find a model not used by agents
            for display_name, model_id in available_models.items():
                if display_name not in used_models and model_id not in used_models:
                    return OpenAIClient(display_name)
            # If all models used, use the latest one anyway
            latest_model = list(available_models.keys())[0]
            return OpenAIClient(latest_model)
        else:
            raise ValueError(f"Unknown company: {company}")
    
    def _create_openrouter_judge_editor(self, used_companies: set, used_models: set) -> Any:
        """
        Create an OpenRouter judge-editor client from an unused company.
        
        Args:
            used_companies: Set of companies already used by agents
            used_models: Set of model IDs already used by agents
            
        Returns:
            OpenRouterClient instance
        """
        from openrouter_client import OpenRouterClient
        
        # Priority order for judge selection
        company_priorities = ['Google', 'Anthropic', 'OpenAI']
        
        for company in company_priorities:
            if company not in used_companies:
                # Search for models from this company
                if company == 'Google':
                    search_terms = ['google', 'gemini']
                elif company == 'Anthropic':
                    search_terms = ['anthropic', 'claude']
                elif company == 'OpenAI':
                    search_terms = ['openai', 'gpt']
                
                for search_term in search_terms:
                    models = OpenRouterClient.search_models(search_term)
                    for model in models:
                        model_id = model['id']
                        if model_id not in used_models:
                            return OpenRouterClient(model_id)
        
        # If no unused company found, use the first available model
        return OpenRouterClient()

    def _create_judge_client(self, provider: str, config: Dict[str, Any] = None) -> Any:
        """
        Create a judge client for the specified provider using latest model.
        
        Args:
            provider: Provider name ('Claude', 'Gemini', 'OpenAI', 'OpenRouter')
            config: Configuration dictionary (needed for OpenRouter routing)
            
        Returns:
            Initialized client instance
        """
        if provider == 'OpenRouter':
            # For OpenRouter, get the latest available model dynamically
            # Search for the latest Claude model through OpenRouter
            from openrouter_client import OpenRouterClient
            claude_models = OpenRouterClient.search_models('claude')
            if claude_models:
                # Use the first (most relevant) Claude model found
                latest_claude = claude_models[0]['id']
                return OpenRouterClient(latest_claude)
            else:
                # If search fails, create client with default and let it handle model selection
                return OpenRouterClient()
        else:
            # For direct API providers, get the latest model dynamically
            if provider == 'Claude':
                from llm_client import LLMClient
                available_models = LLMClient.get_available_models(limit_recent=1)
                latest_model = list(available_models.keys())[0]  # First (newest) model
                return LLMClient(latest_model)
            elif provider == 'Gemini':
                from gemini_client import GeminiClient
                available_models = GeminiClient.get_available_models(limit_recent=1)
                latest_model = list(available_models.keys())[0]  # First (newest) model
                return GeminiClient(latest_model)
            elif provider == 'OpenAI':
                from openai_client import OpenAIClient
                available_models = OpenAIClient.get_available_models(limit_recent=1)
                latest_model = list(available_models.keys())[0]  # First (newest) model
                return OpenAIClient(latest_model)
            else:
                raise ValueError(f"Unknown provider: {provider}")
    
    def generate_critique(self, judge_editor_client: Any, dialogue_data: Dict[str, Any]) -> str:
        """
        Generate a critique of the poetry conversation.
        
        Args:
            judge_editor_client: The judge-editor LLM client
            dialogue_data: Complete dialogue data including conversation history
            
        Returns:
            Critique text from the judge-editor
        """
        critique_prompt = self._create_critique_prompt(dialogue_data)
        
        try:
            critique = judge_client.generate_poetry(critique_prompt, max_tokens=800)
            return critique.strip()
        except Exception as e:
            return f"Error generating critique: {str(e)}"
    
    def edit_conversation(self, judge_client: Any, dialogue_data: Dict[str, Any], critique: str) -> Dict[str, Any]:
        """
        Have the judge edit the conversation based on the critique.
        
        Args:
            judge_client: The judge LLM client
            dialogue_data: Original dialogue data
            critique: The critique generated by the judge
            
        Returns:
            Edited dialogue data with improved conversation
        """
        edit_prompt = self._create_edit_prompt(dialogue_data, critique)
        
        try:
            edited_conversation = judge_client.generate_poetry(edit_prompt, max_tokens=1200)
            
            # Parse the edited conversation back into structured format
            parsed_conversation = self._parse_edited_conversation(edited_conversation.strip(), dialogue_data)
            
            # Create new dialogue data with edited conversation
            edited_dialogue_data = dialogue_data.copy()
            edited_dialogue_data['conversation'] = parsed_conversation
            
            return edited_dialogue_data
            
        except Exception as e:
            # Return original data if editing fails
            print(f"Error editing conversation: {str(e)}")
            return dialogue_data
    
    def _create_critique_prompt(self, dialogue_data: Dict[str, Any]) -> str:
        """Create a prompt for critiquing the poetry conversation using Turner-based rules."""
        
        # Extract conversation details
        theme = dialogue_data['config']['theme']
        form = dialogue_data['config']['form']
        agents = dialogue_data['agents']
        conversation = dialogue_data['conversation']
        
        # Build conversation text
        conversation_text = ""
        for entry in conversation:
            agent_name = entry['agent']
            poetry = entry['poetry']
            conversation_text += f"**{agent_name}:**\n{poetry}\n\n"
        
        # Get Turner-based critique rules
        turner_critique_rules = self.turner_rules.get_critique_rules()
        avoid_list = self.turner_rules.get_avoid_list()
        
        prompt = f"""You are an expert poetry critic and literary scholar specializing in Fred Turner's comprehensive approach to poetry evaluation. Please provide a detailed critique of this poetry conversation between {len(agents)} poets.

**CONVERSATION DETAILS:**
- Theme: {theme}
- Poetic Form: {form}
- Participants: {', '.join(agents)}

**CONVERSATION TO CRITIQUE:**
{conversation_text}

**TURNER-BASED CRITIQUE FRAMEWORK:**
Apply these comprehensive evaluation criteria based on Fred Turner's poetry guidelines:

{turner_critique_rules}

**SPECIFIC ISSUES TO IDENTIFY:**
Look for these common problems:
{chr(10).join(f"- {item}" for item in avoid_list)}

**CRITIQUE INSTRUCTIONS:**
Analyze this poetry conversation and provide constructive feedback on:

1. **Thematic Coherence**: How well does the conversation stay true to the theme of "{theme}"? Does it maintain thematic consistency throughout?

2. **Poetic Form Adherence**: How well do the poems follow the {form} form requirements? Check structural rules, meter, and formal constraints.

3. **Literary Quality & Craft**: 
   - Assess imagery (concrete vs abstract, sensory richness)
   - Evaluate metaphors, similes, and literary devices
   - Analyze word choice and language accessibility
   - Check for archaic language or forced inversions

4. **Emotional Complexity**: 
   - Does the poetry use mixed emotions (positive + negative)?
   - Is there emotional depth and sophistication?
   - Are emotions one-dimensional or complex?

5. **Technical Execution**:
   - Natural scansion and rhythm
   - Appropriate use of rhyme (if any)
   - Flow and readability
   - Effectiveness of endings

6. **Conversational Flow**: How well do the poems respond to and build upon each other?

7. **Character Voice**: Does each poet have a distinct voice and perspective?

8. **Originality**: Are there clichés or overused expressions that should be avoided?

**FORMAT YOUR CRITIQUE:**
Provide a structured critique with clear sections for each area above. Be specific about what works well and what could be improved according to Turner's guidelines. Suggest concrete improvements where possible.

Your critique:"""

        return prompt
    
    def _create_edit_prompt(self, dialogue_data: Dict[str, Any], critique: str) -> str:
        """Create a prompt for editing the conversation based on Turner-based critique and improvement guidelines."""
        
        # Extract conversation details
        theme = dialogue_data['config']['theme']
        form = dialogue_data['config']['form']
        agents = dialogue_data['agents']
        conversation = dialogue_data['conversation']
        
        # Build original conversation text
        original_conversation = ""
        for entry in conversation:
            agent_name = entry['agent']
            poetry = entry['poetry']
            original_conversation += f"**{agent_name}:**\n{poetry}\n\n"
        
        # Get Turner-based editing rules
        turner_editing_rules = self.turner_rules.get_editing_rules()
        enhance_list = self.turner_rules.get_enhance_list()
        avoid_list = self.turner_rules.get_avoid_list()
        
        prompt = f"""Based on your critique, please improve this poetry conversation using Fred Turner's comprehensive poetry improvement guidelines. Keep the same structure and participants, but enhance the poems according to both your critique and Turner's standards.

**ORIGINAL CONVERSATION:**
{original_conversation}

**YOUR CRITIQUE:**
{critique}

**TURNER-BASED IMPROVEMENT GUIDELINES:**
Apply these specific improvement strategies:

{turner_editing_rules}

**ENHANCEMENT PRIORITIES:**
Focus on strengthening these elements:
{chr(10).join(f"- {item}" for item in enhance_list)}

**ELEMENTS TO AVOID/CORRECT:**
Eliminate or improve these issues:
{chr(10).join(f"- {item}" for item in avoid_list)}

**EDITING INSTRUCTIONS:**
1. **Preserve Structure**: Maintain the same theme ({theme}), poetic form ({form}), and participants ({', '.join(agents)})
2. **Keep Organization**: Same number of poems in the same order
3. **Apply Turner Standards**: Use the improvement guidelines above systematically
4. **Enhance Emotional Complexity**: Add mixed emotions (positive + negative) for depth
5. **Improve Imagery**: Replace abstract language with concrete, sensory-rich descriptions
6. **Fix Technical Issues**: Correct scansion, remove forced inversions, strengthen endings
7. **Eliminate Problems**: Remove archaic language, clichés, and awkward phrasing
8. **Maintain Voice**: Preserve distinct character voices while improving quality
9. **Strengthen Coherence**: Enhance thematic connections and conversational flow
10. **Form Compliance**: Ensure strict adherence to {form} requirements

**SPECIFIC FORM GUIDANCE for {form.upper()}:**
- Follow all structural rules precisely
- Pay special attention to meter and rhythm patterns
- Ensure endings are both formally correct and emotionally resonant

**FORMAT YOUR EDITED CONVERSATION:**
Present the improved conversation using this exact format:

**{agents[0]}:**
[improved poem following Turner guidelines]

**{agents[1]}:**
[improved poem following Turner guidelines]

{"**" + agents[0] + ":**" if len(conversation) > 2 else ""}
{"[improved poem following Turner guidelines]" if len(conversation) > 2 else ""}

{"**" + agents[1] + ":**" if len(conversation) > 3 else ""}
{"[improved poem following Turner guidelines]" if len(conversation) > 3 else ""}

Continue this pattern for all poems in the original conversation.

Your edited conversation:"""

        return prompt
    
    def _parse_edited_conversation(self, edited_text: str, original_dialogue_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parse the edited conversation text back into structured format.
        
        Args:
            edited_text: The edited conversation from the judge
            original_dialogue_data: Original dialogue data for structure reference
            
        Returns:
            List of conversation entries in the same format as original
        """
        conversation_entries = []
        original_conversation = original_dialogue_data['conversation']
        
        # Split by agent markers (lines starting with **)
        sections = re.split(r'\n\*\*([^*]+):\*\*\n', edited_text)
        
        # Remove empty first section if present
        if sections and not sections[0].strip():
            sections = sections[1:]
        
        # Parse agent/poetry pairs
        for i in range(0, len(sections) - 1, 2):
            if i + 1 < len(sections):
                agent_name = sections[i].strip()
                poetry = sections[i + 1].strip()
                
                # Find corresponding original entry to preserve metadata
                original_entry = None
                for orig in original_conversation:
                    if orig['agent'] == agent_name:
                        original_entry = orig
                        break
                
                if original_entry:
                    # Create new entry preserving original metadata
                    new_entry = original_entry.copy()
                    new_entry['poetry'] = poetry
                    conversation_entries.append(new_entry)
        
        # If parsing failed, return original conversation
        if len(conversation_entries) != len(original_conversation):
            print("Warning: Could not parse edited conversation properly, using original")
            return original_conversation
        
        return conversation_entries
    
    def critique_and_improve(self, config: Dict[str, Any], dialogue_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete critique and improvement process.
        
        Args:
            config: Configuration dictionary
            dialogue_data: Original dialogue data
            
        Returns:
            Dictionary with original data plus critique and edited conversation
        """
        try:
            # Select judge
            judge_provider, judge_client = self.select_judge(config)
            
            # Generate critique
            critique = self.generate_critique(judge_client, dialogue_data)
            
            # Edit conversation based on critique
            edited_dialogue_data = self.edit_conversation(judge_client, dialogue_data, critique)
            
            # Add critique information to result
            result = dialogue_data.copy()
            result['critique'] = {
                'judge_provider': judge_provider,
                'judge_model': getattr(judge_client, 'model_name', 'Unknown'),
                'critique_text': critique,
                'edited_conversation': edited_dialogue_data['conversation']
            }
            
            return result
            
        except Exception as e:
            print(f"Error in critique process: {str(e)}")
            # Return original data with error message
            result = dialogue_data.copy()
            result['critique'] = {
                'judge_provider': 'Error',
                'judge_model': 'N/A',
                'critique_text': f"Error generating critique: {str(e)}",
                'edited_conversation': dialogue_data['conversation']
            }
            return result