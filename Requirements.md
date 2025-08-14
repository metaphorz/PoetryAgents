# Poetry Agent Dialogue

## Software Requirements

Use Git version control by init when the project is created
Create a .gitignore file and when pushing to GitHub, do not push the .gitignore file 
Period requests to commit will be given by the user, so do not run git commit automatically
Always work in the main branch unless requested to make a new branch, with later merge

When requested to refactor or test by the user, proceed with minimal user interaction
Keep all tests and test results in a /tests directory
After each refactor and tests, commit to Git

## Overview

This project simulates a system where two AI agents can communicate by exchanging text. Thus, the system is a generator of a dialogue. Agent's have randomly selected names from fictional characters of famous novels. Just use first names. 

## Software Architecture

The system supports multiple LLM providers for generating poetry:
- **Claude Sonnet 4** (Anthropic) - Primary LLM
- **Gemini 2.5 Pro** (Google)
- **OpenAI O3 Mini** (OpenAI)
- **OpenRouter** - Unified access to multiple LLM providers

### Auto-Critique System

The system includes an intelligent auto-critique feature that automatically evaluates and improves poetry conversations:

1. **Judge LLM Selection**: The system automatically selects a "judge" LLM that is different from the LLMs used in the conversation
   - For direct API mode (option 1): Judge selects from unused providers among Claude, OpenAI, and Gemini
   - For OpenRouter mode (option 2): Judge uses OpenRouter with Claude Sonnet as the judge model
   
2. **Critique Process**:
   - Judge analyzes the original conversation for thematic coherence, poetic form adherence, literary quality, conversational flow, and character voice
   - Provides detailed structured critique with specific feedback
   - Creates an improved version of the conversation based on the critique
   
3. **Enhanced Output**: The markdown output includes three sections:
   - **Original Conversation**: The initial poetry dialogue
   - **Literary Critique**: Detailed analysis from the judge LLM
   - **Revised Conversation**: Improved version based on the critique

### LLM Routing Logic

- **Option 1 (Direct APIs)**: Uses provider-specific API keys and latest models
- **Option 2 (OpenRouter)**: Routes all requests through OpenRouter API
- **Judge Consistency**: Judge uses the same routing mechanism as conversation agents

In addition, if the LLM needs other software to perform its task, bring this to the attention of the user. For example, some parsing software may count syllables or search for semantically related words.

Write only as much software (code) as necessary, while maximally leveraging the LLM to obtain each component of the dialogue.

Do not use any simulated code or mock/substitute code. Just perform as these instructions.

## User Interface

### Questions

The interface asks the user specific questions before generating the dialogue:

1. what is the theme?
2. How many agents are there?
3. What is the form of dialogue?
4. What is the length of each poem?
5. What is the length of the conversation?

### Question Descriptions

1. Theme: the user provides a set of words or a phrase or sentence. As an example, the user says "A walk in the snow"
2. Agents: the user provides a number of agents. As an example, the user says "2"
3. Form: the user provides a form of dialogue. You should just do haiku or prose for now. Haiku is a rigid format of 5-7-5 syllables. Prose is free verse.
4. Poem Length: the user provides a length of dialogue in lines. As an example, the user says "6"  meaning a haiku of 2 parts (3 lines per part). For prose, the user says "6" meaning 6 lines of prose for each speaker.
5. Conversation Length: the user provides a length of dialogue in poems.  As an example, the user says "2" meaning that each agent will have 2 poems, comprising 4 poems total.
 
## Poetic Form

Each poetic form has rules. These rules embed the concepts of meter and rhyme. Abide by the rules of the poetic form.

Do not put in additional text such as "Here is a poem" or "I'll craft a Haiku". Just put in the poetry headed by the agent's name

Always put a blank space after each verse, and if multiple poems are in an agent response, put a blank space after each poem (e.g. for haikus)

## Dialogue Format

The first agent to create its poetry will base this poetry on the user's theme. Each subsequent agent will base its poetry on the poetry of the previous agent. A dialogue operates in this fashion. Basing poetry on the previous agent can be done by reusing a phrase or word, or words previously spoken.

## Example

1. what is the theme? a walk in the snow
2. How many agents are there?
3. What is the form of dialogue?
4. What is the length of each poem?
5. What is the length of the conversation? 1

This generates the following output, starting with a title.

Winter Walk (in larger bold font)
[this title is made from the user's theme]

Alpha: (in bold)
[Here is what I entered: make a haiku that is of 2 stanzas about a walk in the snow]
[this is in a format of make a <form entered by user> about a <theme entered by user>]
[this will end up coded as a request based on a prompt to the LLM]

Fresh snow crunches soft
Beneath my careful footsteps—
Silent world awaits

Breath clouds drift and fade
While bare branches frame the sky
Peace in winter's grip

Beta:
[I entered: Now imagine this haiku was spoken by an agent called Alpha. Beta now responds to Alpha. This response is based in some way on what Alpha has said. Go ahead]

Your tracks mark the path
I follow through drifted white—
Two souls, one winter

Where you found silence
I hear whispers in the wind
Speaking of spring's hope

[If not limited by the user's length of conversation, this process would continue]
[your code is simply a scaffold around prompts to the LLM]


## Example: Villanelle Dialogue

**Theme:** "Walking on Icelandic Ice"  
**Agents:** 2 (Pierre, Scout)  
**Form:** Villanelle  
**Poem Length:** 19 lines  
**Conversation Length:** 2 rounds

---

### Pierre:
*(A1)* Beneath the northern sky, I sought my way,  
the wind reciting sermons to the stone,  
*(A2)* and in that hush, the soul forgot to pray.  

The ice beneath my steps began to sway,  
as if it knew the path was not my own;  
Beneath the northern sky, I sought my way.  

The mountains kept their counsel, cold and gray,  
their gaze more ancient than a monarch’s throne,  
and in that hush, the soul forgot to pray.  

A river murmured truths I could not weigh,  
its voice as fleeting as a breath half-blown;  
Beneath the northern sky, I sought my way.  

I thought of home, of hearts that could not stay,  
of love that thaws, then chills to polished bone,  
and in that hush, the soul forgot to pray.  

Perhaps the meaning comes on such a day,  
when all that speaks is wind, and all alone—  
Beneath the northern sky, I sought my way,  
and in that hush, the soul forgot to pray.

---

### Scout:
The ice beneath our feet knows how to sway,  
like courthouse floors when verdicts make men small—  
the mockingbirds have nothing left to say.  

I've watched the grown-ups tremble, kneel, and pray,  
their certainties like snow about to fall;  
the ice beneath our feet knows how to sway.  

In Maycomb's heat or Iceland's endless gray,  
the same cold truth makes cowards of us all—  
the mockingbirds have nothing left to say.  

Atticus once taught me right from stray,  
but even he can't catch what slips the wall;  
the ice beneath our feet knows how to sway.  

I've seen men judged like shadows in a play,  
their innocence a ghost inside the hall—  
the mockingbirds have nothing left to say.  

Perhaps we're all just learning how to weigh  
what breaks beneath, what answers when we call;  
the ice beneath our feet knows how to sway,  
the mockingbirds have nothing left to say.

---

**Notes for Developers/Testers:**  
- Check that A1 and A2 are repeated exactly as required by the form rules.  
- Ensure both agents share thematic and imagery links (here: "ice", "sway", moral uncertainty).  
- Verify emotional arc: Pierre’s introspection → Scout’s moral realism.  
