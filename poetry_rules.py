"""
Comprehensive structural rules for all poetry forms.
These rules provide detailed guidance to LLMs for proper adherence to poetic structures.
"""

def get_poetry_rules(form: str) -> str:
    """
    Get comprehensive structural rules for a specific poetry form.
    
    Args:
        form: Poetry form (haiku, prose, sonnet, villanelle, limerick, ballad, ghazal, tanka)
        
    Returns:
        Detailed structural rules as a string
    """
    
    rules = {
        "haiku": """
HAIKU STRUCTURAL RULES:
• EXACTLY 3 lines
• Syllable pattern: 5-7-5 (line 1: 5 syllables, line 2: 7 syllables, line 3: 5 syllables)
• Total of 17 syllables across all lines
• Present tense preferred
• Focus on nature, seasons, or moments of awareness
• No rhyming required
• Capture a single moment or image
• Often includes a "cutting word" or pause
• Example syllable counting: "Au-tumn leaves fall-ing" (5), "Gen-tly to the qui-et earth" (7), "Si-lent beau-ty" (5)

SYLLABLE COUNTING GUIDE:
• Count vowel sounds, not letters
• "Beautiful" = beau-ti-ful = 3 syllables
• "Flower" = flow-er = 2 syllables
• "Fire" = 1 syllable (single vowel sound)
• "Quietly" = qui-et-ly = 3 syllables

FORMAT: Present as exactly 3 lines with no additional text.
""",

        "sonnet": """
SONNET STRUCTURAL RULES (Shakespearean):
• EXACTLY 14 lines
• Rhyme scheme: ABAB CDCD EFEF GG
• Meter: Iambic pentameter (10 syllables per line, unstressed-stressed pattern)
• Structure: 3 quatrains (4-line stanzas) + 1 couplet (2 lines)
• Quatrain 1 (lines 1-4): Introduce theme/problem
• Quatrain 2 (lines 5-8): Develop/complicate theme
• Quatrain 3 (lines 9-12): Climax/turn (volta)
• Couplet (lines 13-14): Resolution/conclusion with final rhyme

IAMBIC PENTAMETER GUIDE:
• 10 syllables per line in da-DUM da-DUM da-DUM da-DUM da-DUM pattern
• Example: "Shall I com-PARE thee TO a SUM-mer's DAY?"
• Unstressed-stressed, unstressed-stressed, repeat 5 times

RHYME SCHEME EXAMPLE:
Line 1: "day" (A)    Line 9: "eyes" (E)
Line 2: "face" (B)   Line 10: "art" (F)
Line 3: "way" (A)    Line 11: "skies" (E)
Line 4: "grace" (B)  Line 12: "heart" (F)
Line 5: "light" (C)  Line 13: "true" (G)
Line 6: "time" (D)   Line 14: "you" (G)
Line 7: "night" (C)
Line 8: "rhyme" (D)

FORMAT: Present as 14 lines with no stanza breaks.
""",

        "villanelle": """
VILLANELLE STRUCTURAL RULES:
• EXACTLY 19 lines
• 5 tercets (3-line stanzas) + 1 quatrain (4-line stanza)
• Only 2 rhymes used throughout entire poem
• 2 refrains (repeated lines): A1 and A2
• Pattern: A1bA2 abA1 abA2 abA1 abA2 abA1A2

REFRAIN RULES:
• A1 = Line 1, repeated as lines 6, 12, 18
• A2 = Line 3, repeated as lines 9, 15, 19
• Both refrains must rhyme with each other
• All "b" lines must rhyme with each other

STRUCTURE BREAKDOWN:
Tercet 1: A1(refrain) b A2(refrain)
Tercet 2: a b A1(refrain)
Tercet 3: a b A2(refrain)  
Tercet 4: a b A1(refrain)
Tercet 5: a b A2(refrain)
Quatrain: a b A1(refrain) A2(refrain)

EXAMPLE PATTERN:
Line 1: "Do not go gentle into that good night" (A1)
Line 2: "Old age should burn and rave at close of day" (b)
Line 3: "Rage, rage against the dying of the light" (A2)
...continues with pattern...

FORMAT: Present as 6 stanzas (5 tercets + 1 quatrain) with line breaks between stanzas.
""",

        "limerick": """
LIMERICK STRUCTURAL RULES:
• EXACTLY 5 lines
• Rhyme scheme: AABBA
• Meter: Anapestic (da-da-DUM rhythm)
• Lines 1, 2, 5: Longer (8-10 syllables)
• Lines 3, 4: Shorter (5-7 syllables)
• Humorous, witty, or nonsensical content
• Often begins with "There once was a..." or "A [person] from [place]..."

METER PATTERN:
• Lines 1, 2, 5: da-da-DUM da-da-DUM da-da-DUM
• Lines 3, 4: da-da-DUM da-da-DUM
• Example: "There ONCE was a MAN from Nan-TUCK-et" (line 1)
• Example: "His BEARD was so LONG" (line 3)

RHYME SCHEME EXAMPLE:
Line 1: "Nantucket" (A)
Line 2: "bucket" (A)  
Line 3: "long" (B)
Line 4: "strong" (B)
Line 5: "tucket" (A)

CONTENT GUIDELINES:
• Light-hearted, playful tone
• Often includes wordplay or puns
• May be absurd or fantastical
• Surprise or twist in final line

FORMAT: Present as 5 lines with no stanza breaks.
""",

        "ballad": """
BALLAD STRUCTURAL RULES:
• Multiple quatrains (4-line stanzas)
• Rhyme scheme: ABAB or ABCB (second pattern more common)
• Meter: Alternating iambic tetrameter and trimeter
• Lines 1, 3: 8 syllables (iambic tetrameter)
• Lines 2, 4: 6 syllables (iambic trimeter)
• Narrative structure (tells a story)
• Often includes dialogue, repetition, or refrains

METER PATTERN:
• Line 1: da-DUM da-DUM da-DUM da-DUM (8 syllables)
• Line 2: da-DUM da-DUM da-DUM (6 syllables)
• Line 3: da-DUM da-DUM da-DUM da-DUM (8 syllables)
• Line 4: da-DUM da-DUM da-DUM (6 syllables)

NARRATIVE ELEMENTS:
• Plot progression across stanzas
• Character development
• Dialogue (often unmarked)
• Dramatic events or conflicts
• Resolution or tragic ending

RHYME SCHEME EXAMPLE (ABCB):
Line 1: "story" (A)
Line 2: "night" (B)
Line 3: "worry" (C)
Line 4: "bright" (B)

TRADITIONAL THEMES:
• Love and loss
• Adventure and heroism
• Supernatural events
• Historical events
• Folk tales and legends

FORMAT: Present as multiple quatrains with line breaks between stanzas.
""",

        "ghazal": """
GHAZAL STRUCTURAL RULES:
• 5-15 couplets (sher), each couplet is independent
• Each couplet has 2 lines of equal length
• Monorhyme: All second lines end with same rhyme + radif
• Radif: Repeated word/phrase at end of each couplet's second line
• Qafia: Rhyme word before the radif
• Traditional themes: love, loss, longing, separation, spiritual yearning

STRUCTURE PATTERN:
• Line 1: [text] qafia radif
• Line 2: [text] qafia radif
• Line 3: [text] [different content]
• Line 4: [text] qafia radif
• Continue pattern...

RADIF EXAMPLES:
• "...in the night" (radif = "in the night")
• "...of love" (radif = "of love")
• "...away" (radif = "away")

QAFIA + RADIF EXAMPLES:
• "pain of love" (qafia = "pain", radif = "of love")
• "lost in the night" (qafia = "lost", radif = "in the night")
• "drift away" (qafia = "drift", radif = "away")

COUPLET INDEPENDENCE:
• Each couplet should express complete thought
• Can be read alone and still make sense
• Connected by theme, not narrative sequence

TRADITIONAL ELEMENTS:
• Beloved (often unattainable)
• Separation and longing
• Wine and intoxication (metaphorical)
• Garden imagery (roses, nightingales)
• Spiritual seeking

FORMAT: Present as couplets with line breaks between each couplet.
""",

        "tanka": """
TANKA STRUCTURAL RULES:
• EXACTLY 5 lines
• Syllable pattern: 5-7-5-7-7
• Total of 31 syllables
• Two-part structure with pivot (usually after line 2 or 3)
• Upper phrase (lines 1-3): 5-7-5 syllables
• Lower phrase (lines 4-5): 7-7 syllables
• Traditional themes: nature, seasons, love, impermanence

SYLLABLE BREAKDOWN:
• Line 1: 5 syllables
• Line 2: 7 syllables  
• Line 3: 5 syllables
• Line 4: 7 syllables
• Line 5: 7 syllables

PIVOT STRUCTURE:
• Upper phrase sets scene/image
• Lower phrase provides reflection/emotion
• Pivot creates turn or shift in perspective
• Example: Nature image → Personal reflection

SYLLABLE COUNTING GUIDE:
• Same as haiku: count vowel sounds
• "Cherry blossoms" = cher-ry blos-soms = 4 syllables
• "Moonlight" = moon-light = 2 syllables
• "Gently" = gent-ly = 2 syllables

TRADITIONAL THEMES:
• Seasonal observations
• Emotional responses to nature
• Love and relationships
• Impermanence and change
• Moments of awareness or insight

FORMAT: Present as exactly 5 lines with no stanza breaks.
""",

        "prose": """
PROSE POEM STRUCTURAL RULES:
• Written in paragraph form (no line breaks)
• Combines poetic language with prose format
• Maintains poetic devices: imagery, metaphor, rhythm
• Length varies by user specification
• No rhyme scheme required
• Focus on lyrical, evocative language

POETIC ELEMENTS TO INCLUDE:
• Vivid imagery and sensory details
• Metaphors and similes
• Alliteration, assonance, consonance
• Rhythmic language patterns
• Emotional resonance
• Symbolic meaning

PROSE POEM CHARACTERISTICS:
• Compressed, concentrated language
• Every word carries weight
• Blends narrative with lyrical elements
• May include fragmented thoughts
• Stream-of-consciousness style acceptable
• Rich, descriptive language

STRUCTURE GUIDELINES:
• Use paragraph breaks for multiple sections
• Maintain internal rhythm and flow
• Build toward emotional or thematic climax
• Create unity through recurring images/themes
• Balance concrete details with abstract concepts

LANGUAGE TECHNIQUES:
• Repetition for emphasis
• Parallel structure
• Varied sentence lengths
• Sensory details
• Unexpected juxtapositions
• Symbolic imagery

FORMAT: Present as paragraph(s) with proper punctuation and no line breaks within paragraphs.
"""
    }
    
    return rules.get(form, f"No specific rules available for {form} form.")

def get_formatting_rules() -> str:
    """Get general formatting rules that apply to all poetry forms."""
    return """
GENERAL FORMATTING RULES:
• Return ONLY the poem with no explanatory text
• No title unless specifically requested
• No author attribution
• No commentary or analysis
• Follow exact line/stanza structure for the form
• Use proper punctuation where appropriate
• Maintain consistent capitalization style
• End with appropriate spacing as specified
"""

def get_quality_guidelines() -> str:
    """Get general quality guidelines for all poetry."""
    return """
QUALITY GUIDELINES:
• Use vivid, specific imagery
• Avoid clichés and overused phrases
• Choose precise, evocative words
• Create emotional resonance
• Maintain thematic consistency
• Use literary devices appropriately
• Ensure grammatical correctness
• Make every word count
• Create unity and coherence
• Surprise the reader while staying true to form
"""