"""
Turner-Based Poetry Rules Management System
Manages comprehensive poetry creation and critique guidelines based on Fred Turner's expertise.
"""

from typing import Dict, List, Any


class TurnerRulesManager:
    """Manages Turner-based poetry rules for judge system integration."""
    
    def __init__(self):
        """Initialize with structured Turner rules."""
        self.rules = self._load_rules()
    
    def _load_rules(self) -> Dict[str, List[Dict[str, str]]]:
        """Load and structure Turner-based poetry rules."""
        return {
            "language_style": [
                {
                    "id": "TS1",
                    "title": "Avoid Archaic Language",
                    "rule": "Do not use archaic words: o'er, thee, thou, behest, or forsooth",
                    "critique_focus": "Check for archaic language usage",
                    "edit_guidance": "Replace archaic terms with modern, accessible language"
                },
                {
                    "id": "TS2", 
                    "title": "Prefer Concrete Words",
                    "rule": "Use concrete words over abstract words for stronger imagery",
                    "critique_focus": "Assess balance of concrete vs abstract language",
                    "edit_guidance": "Replace abstract concepts with tangible, specific imagery"
                },
                {
                    "id": "TS3",
                    "title": "Use Idiomatic Language",
                    "rule": "Employ natural, conversational phrasing unless heightened diction is required",
                    "critique_focus": "Evaluate naturalness and accessibility of language",
                    "edit_guidance": "Rewrite awkward or unnatural phrases with idiomatic expressions"
                },
                {
                    "id": "TS4",
                    "title": "Avoid Forced Inversions", 
                    "rule": "Refrain from inverting natural word order just to meet rhyming or metrical constraints",
                    "critique_focus": "Identify awkward word order inversions",
                    "edit_guidance": "Restructure lines to maintain natural syntax while preserving form"
                }
            ],
            
            "emotional_thematic": [
                {
                    "id": "ET1",
                    "title": "Use Mixed Emotions",
                    "rule": "Combine positive and negative emotions to create unique emotional mixes that put things in new light",
                    "critique_focus": "Analyze emotional complexity and balance",
                    "edit_guidance": "Add contrasting emotions to create depth and complexity"
                },
                {
                    "id": "ET2",
                    "title": "Balance Emotional Tones",
                    "rule": "Combine contrasting emotions (love/doubt, joy/melancholy) for thematic depth",
                    "critique_focus": "Evaluate emotional range and sophistication",
                    "edit_guidance": "Introduce emotional counterpoints to avoid one-dimensional expression"
                },
                {
                    "id": "ET3",
                    "title": "Maintain Thematic Coherence",
                    "rule": "Keep the poem's central theme clear throughout, even in complex forms",
                    "critique_focus": "Assess thematic consistency and clarity",
                    "edit_guidance": "Strengthen thematic connections between stanzas and sections"
                }
            ],
            
            "technical_craft": [
                {
                    "id": "TC1",
                    "title": "Use Visual/Sensory Imagery",
                    "rule": "Employ vivid, sensory descriptions that evoke emotions and scenes effectively",
                    "critique_focus": "Evaluate strength and specificity of imagery",
                    "edit_guidance": "Replace generic expressions with specific, sensory-rich descriptions"
                },
                {
                    "id": "TC2",
                    "title": "Use Appropriate Tropes",
                    "rule": "Use metaphors and similes when appropriate to enhance meaning",
                    "critique_focus": "Assess effectiveness of literary devices",
                    "edit_guidance": "Add or refine metaphors and similes for greater impact"
                },
                {
                    "id": "TC3",
                    "title": "Handle Rhyme Thoughtfully",
                    "rule": "Avoid rhyming unless requested; use occasional rhyming words for flow in free verse",
                    "critique_focus": "Evaluate rhyme scheme appropriateness and execution",
                    "edit_guidance": "Adjust rhyming to serve the poem's flow and meaning, not force it"
                }
            ],
            
            "formal_structure": [
                {
                    "id": "FS1", 
                    "title": "Adhere to Poetic Form",
                    "rule": "Respect structural rules of specific forms (sestinas, sonnets, villanelles)",
                    "critique_focus": "Check strict adherence to form requirements",
                    "edit_guidance": "Correct form violations while preserving meaning and flow"
                },
                {
                    "id": "FS2",
                    "title": "Maintain Natural Scansion",
                    "rule": "Ensure lines flow smoothly and adhere to intended meter without awkward phrasing",
                    "critique_focus": "Analyze rhythm, meter, and flow of lines",
                    "edit_guidance": "Adjust phrasing to improve scansion while maintaining meaning"
                },
                {
                    "id": "FS3",
                    "title": "Pay Attention to Endings",
                    "rule": "Ensure conclusions resonate emotionally and adhere to form rules",
                    "critique_focus": "Evaluate effectiveness and form-compliance of endings",
                    "edit_guidance": "Strengthen endings for emotional impact and formal completion"
                },
                {
                    "id": "FS4",
                    "title": "Consider Poem Structure",
                    "rule": "The poem need not be merely descriptive; explore narrative, emotional, or philosophical dimensions",
                    "critique_focus": "Assess structural variety and purpose beyond description",
                    "edit_guidance": "Expand beyond description to include narrative or reflective elements"
                }
            ],
            
            "quality_refinement": [
                {
                    "id": "QR1",
                    "title": "Avoid Clichés",
                    "rule": "Avoid overused phrases and expressions that lack originality",
                    "critique_focus": "Identify clichéd language and tired expressions", 
                    "edit_guidance": "Replace clichés with fresh, original expressions"
                },
                {
                    "id": "QR2",
                    "title": "Iterate to Perfection",
                    "rule": "Poetry requires revision to align with formal constraints, thematic intent, and emotional resonance",
                    "critique_focus": "Evaluate overall need for refinement and improvement",
                    "edit_guidance": "Apply multiple revision passes to perfect craft and meaning"
                }
            ]
        }
    
    def get_critique_rules(self) -> str:
        """Get formatted Turner rules for critique prompts."""
        formatted_rules = []
        
        for category, rules in self.rules.items():
            category_name = category.replace('_', ' ').title()
            formatted_rules.append(f"**{category_name}:**")
            
            for rule in rules:
                formatted_rules.append(f"- **{rule['title']}**: {rule['critique_focus']}")
        
        return "\n".join(formatted_rules)
    
    def get_editing_rules(self) -> str:
        """Get formatted Turner rules for editing prompts."""
        formatted_rules = []
        
        for category, rules in self.rules.items():
            category_name = category.replace('_', ' ').title()
            formatted_rules.append(f"**{category_name}:**")
            
            for rule in rules:
                formatted_rules.append(f"- **{rule['title']}**: {rule['edit_guidance']}")
        
        return "\n".join(formatted_rules)
    
    def get_rules_by_category(self, category: str) -> List[Dict[str, str]]:
        """Get rules for a specific category."""
        return self.rules.get(category, [])
    
    def get_all_categories(self) -> List[str]:
        """Get list of all rule categories."""
        return list(self.rules.keys())
    
    def get_avoid_list(self) -> List[str]:
        """Get list of things to avoid based on Turner rules."""
        avoid_items = [
            "Archaic language (o'er, thee, thou, behest, forsooth)",
            "Abstract language without concrete imagery",
            "Forced word order inversions",
            "One-dimensional emotions",
            "Generic or vague descriptions", 
            "Inappropriate or forced rhyming",
            "Form rule violations",
            "Awkward rhythm or scansion",
            "Weak or unsatisfying endings",
            "Clichéd expressions",
            "Overly complex metaphors"
        ]
        return avoid_items
    
    def get_enhance_list(self) -> List[str]:
        """Get list of things to enhance based on Turner rules."""
        enhance_items = [
            "Mixed emotional complexity (positive + negative)",
            "Concrete, sensory-rich imagery",
            "Natural, idiomatic language",
            "Thematic coherence throughout",
            "Appropriate metaphors and similes",
            "Natural scansion and rhythm",
            "Strong, resonant endings",
            "Form-specific structural elements",
            "Original, fresh expressions",
            "Narrative or philosophical depth beyond description"
        ]
        return enhance_items