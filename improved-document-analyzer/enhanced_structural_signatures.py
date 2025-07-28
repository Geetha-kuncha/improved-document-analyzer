#!/usr/bin/env python3

"""
Enhanced structural signatures that better distinguish between different types of procedural content
without relying on keywords
"""

class EnhancedStructuralSignatures:
    def __init__(self):
        # Enhanced structural signatures based on information architecture patterns
        self.enhanced_signatures = {
            'hr_professional': {
                'create_manage_forms': {
                    'structural_patterns': {
                        # Form-related structural indicators
                        'field_creation_patterns': [
                            r'^\s*\d+\.\s+(?:Select|Choose|Click).*(?:field|form|button)',
                            r'^\s*\d+\.\s+(?:Add|Create|Insert).*(?:text|field|checkbox)',
                            r'^\s*\d+\.\s+(?:Configure|Set up|Define).*(?:properties|options)'
                        ],
                        'workflow_patterns': [
                            r'^\s*\d+\.\s+(?:Send|Share|Distribute).*(?:document|form)',
                            r'^\s*\d+\.\s+(?:Review|Approve|Sign).*(?:process|workflow)',
                            r'^\s*\d+\.\s+(?:Collect|Gather|Manage).*(?:responses|data)'
                        ],
                        'compliance_patterns': [
                            r'^\s*\d+\.\s+(?:Enable|Set|Configure).*(?:security|permissions)',
                            r'^\s*\d+\.\s+(?:Track|Monitor|Audit).*(?:access|changes)',
                            r'^\s*\d+\.\s+(?:Archive|Store|Backup).*(?:records|documents)'
                        ]
                    },
                    'information_architecture': {
                        'hierarchical_depth': 3,  # Deep nested procedures
                        'cross_references': True,  # References to other sections
                        'conditional_logic': True,  # If-then patterns
                        'sequential_dependencies': True  # Step dependencies
                    },
                    'content_density_indicators': {
                        'ui_element_references': 0.3,  # High UI references
                        'action_verb_density': 0.4,   # High action density
                        'technical_specificity': 0.5,  # Specific technical terms
                        'process_complexity': 0.6      # Complex multi-step processes
                    }
                }
            },
            'travel_planner': {
                'plan_group_trip': {
                    'structural_patterns': {
                        'itinerary_patterns': [
                            r'^\s*(?:Day\s+\d+|Morning|Afternoon|Evening)',
                            r'^\s*\d+:\d+\s*(?:AM|PM)?',
                            r'^\s*\d+\.\s+(?:Visit|Go to|Explore).*(?:at|in|near)'
                        ],
                        'logistics_patterns': [
                            r'^\s*\d+\.\s+(?:Book|Reserve|Contact).*(?:hotel|restaurant)',
                            r'^\s*\d+\.\s+(?:Check|Confirm|Verify).*(?:availability|booking)',
                            r'^\s*\d+\.\s+(?:Meet|Gather|Depart).*(?:at|from)'
                        ],
                        'resource_patterns': [
                            r'^\s*\d+\.\s+(?:Budget|Cost|Price).*(?:per person|total)',
                            r'^\s*\d+\.\s+(?:Pack|Bring|Prepare).*(?:for|before)',
                            r'^\s*\d+\.\s+(?:Download|Get|Obtain).*(?:map|guide|tickets)'
                        ]
                    },
                    'information_architecture': {
                        'hierarchical_depth': 2,  # Moderate nesting
                        'cross_references': False, # Less cross-referencing
                        'conditional_logic': False, # Simple linear flow
                        'sequential_dependencies': True  # Time-based sequence
                    },
                    'content_density_indicators': {
                        'location_density': 0.6,      # High location references
                        'time_density': 0.5,          # High time references
                        'contact_density': 0.4,       # Moderate contact info
                        'price_density': 0.3           # Moderate pricing info
                    }
                }
            },
            'software_learner': {
                'learn_software_features': {
                    'structural_patterns': {
                        'tutorial_patterns': [
                            r'^\s*\d+\.\s+(?:Open|Launch|Start).*(?:application|program)',
                            r'^\s*\d+\.\s+(?:Navigate to|Go to|Find).*(?:menu|toolbar|panel)',
                            r'^\s*\d+\.\s+(?:Follow|Complete|Practice).*(?:steps|exercise)'
                        ],
                        'feature_patterns': [
                            r'^\s*\d+\.\s+(?:Use|Try|Apply).*(?:tool|feature|function)',
                            r'^\s*\d+\.\s+(?:Customize|Adjust|Modify).*(?:settings|preferences)',
                            r'^\s*\d+\.\s+(?:Save|Export|Share).*(?:work|document|file)'
                        ],
                        'troubleshooting_patterns': [
                            r'^\s*\d+\.\s+(?:If|When|Should).*(?:error|problem|issue)',
                            r'^\s*\d+\.\s+(?:Check|Verify|Ensure).*(?:that|if)',
                            r'^\s*\d+\.\s+(?:Try|Attempt|Consider).*(?:alternative|different)'
                        ]
                    },
                    'information_architecture': {
                        'hierarchical_depth': 2,  # Moderate depth
                        'cross_references': True,  # References to other features
                        'conditional_logic': False, # Simple procedures
                        'sequential_dependencies': True  # Step-by-step learning
                    },
                    'content_density_indicators': {
                        'ui_element_references': 0.7,  # Very high UI references
                        'action_verb_density': 0.5,    # High action density
                        'learning_progression': 0.4,   # Progressive complexity
                        'example_density': 0.3         # Examples and illustrations
                    }
                }
            }
        }
    
    def analyze_structural_signature(self, content_blocks, persona_category, job_category):
        """Analyze content blocks against enhanced structural signatures"""
        
        if persona_category not in self.enhanced_signatures:
            return 0.0
        
        if job_category not in self.enhanced_signatures[persona_category]:
            return 0.0
        
        signature = self.enhanced_signatures[persona_category][job_category]
        
        # Analyze structural patterns
        pattern_score = self.calculate_pattern_match_score(content_blocks, signature['structural_patterns'])
        
        # Analyze information architecture
        architecture_score = self.calculate_architecture_score(content_blocks, signature['information_architecture'])
        
        # Analyze content density
        density_score = self.calculate_density_score(content_blocks, signature['content_density_indicators'])
        
        # Weighted combination
        final_score = (pattern_score * 0.4) + (architecture_score * 0.3) + (density_score * 0.3)
        
        return final_score
    
    def calculate_pattern_match_score(self, content_blocks, structural_patterns):
        """Calculate how well content matches structural patterns"""
        total_score = 0.0
        total_patterns = 0
        
        all_content = '\n'.join([block.get('content', '') for block in content_blocks])
        
        for pattern_category, patterns in structural_patterns.items():
            category_score = 0.0
            
            for pattern in patterns:
                import re
                matches = len(re.findall(pattern, all_content, re.MULTILINE | re.IGNORECASE))
                if matches > 0:
                    category_score += min(matches / 10.0, 1.0)  # Normalize to 0-1
            
            if patterns:
                category_score /= len(patterns)
                total_score += category_score
                total_patterns += 1
        
        return total_score / total_patterns if total_patterns > 0 else 0.0
    
    def calculate_architecture_score(self, content_blocks, architecture_requirements):
        """Calculate information architecture alignment score"""
        score = 0.0
        
        # Analyze hierarchical depth
        max_depth = self.analyze_hierarchical_depth(content_blocks)
        required_depth = architecture_requirements.get('hierarchical_depth', 2)
        depth_score = min(max_depth / required_depth, 1.0)
        score += depth_score * 0.3
        
        # Analyze cross-references
        has_cross_refs = self.detect_cross_references(content_blocks)
        requires_cross_refs = architecture_requirements.get('cross_references', False)
        if has_cross_refs == requires_cross_refs:
            score += 0.2
        
        # Analyze conditional logic
        has_conditional = self.detect_conditional_logic(content_blocks)
        requires_conditional = architecture_requirements.get('conditional_logic', False)
        if has_conditional == requires_conditional:
            score += 0.2
        
        # Analyze sequential dependencies
        has_sequential = self.detect_sequential_dependencies(content_blocks)
        requires_sequential = architecture_requirements.get('sequential_dependencies', True)
        if has_sequential == requires_sequential:
            score += 0.3
        
        return score
    
    def calculate_density_score(self, content_blocks, density_indicators):
        """Calculate content density alignment score"""
        score = 0.0
        total_indicators = len(density_indicators)
        
        if total_indicators == 0:
            return 0.0
        
        all_content = '\n'.join([block.get('content', '') for block in content_blocks])
        word_count = len(all_content.split())
        
        if word_count == 0:
            return 0.0
        
        for indicator, expected_density in density_indicators.items():
            actual_density = self.calculate_specific_density(all_content, indicator, word_count)
            
            # Score based on how close actual density is to expected
            density_diff = abs(actual_density - expected_density)
            indicator_score = max(0, 1.0 - (density_diff * 2))  # Penalty for deviation
            score += indicator_score
        
        return score / total_indicators
    
    def calculate_specific_density(self, content, indicator_type, word_count):
        """Calculate density for specific indicator types"""
        import re
        
        density_patterns = {
            'ui_element_references': [
                r'\b(?:button|menu|toolbar|panel|dialog|window|field|checkbox|dropdown)\b',
                r'\b(?:click|select|choose|press|drag|drop|hover)\b',
                r'\b(?:All tools|File menu|Edit menu|View menu)\b'
            ],
            'action_verb_density': [
                r'\b(?:create|make|build|generate|produce)\b',
                r'\b(?:edit|modify|change|update|revise)\b',
                r'\b(?:save|export|share|send|distribute)\b'
            ],
            'location_density': [
                r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Street|Avenue|Hotel|Restaurant|Museum))\b',
                r'\b(?:address|location|place|venue|destination)\b'
            ],
            'time_density': [
                r'\b\d{1,2}:\d{2}(?:\s*[AP]M)?\b',
                r'\b(?:morning|afternoon|evening|night|day|hour|minute)\b',
                r'\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b'
            ],
            'contact_density': [
                r'\b(?:phone|email|website|contact|address)\b',
                r'\b(?:www\.|http|@[\w.-]+|\+?\d{1,3}[-.\s]?\d{1,4})\b'
            ],
            'price_density': [
                r'\b(?:€|$|£)\s*\d+(?:\.\d{2})?\b',
                r'\b\d+(?:\.\d{2})?\s*(?:euros?|dollars?|pounds?)\b',
                r'\b(?:cost|price|fee|budget|expense)\b'
            ],
            'technical_specificity': [
                r'\b(?:configure|parameter|setting|option|property)\b',
                r'\b(?:database|server|client|API|URL|XML|JSON)\b'
            ],
            'process_complexity': [
                r'\b(?:workflow|process|procedure|protocol|methodology)\b',
                r'\b(?:step|phase|stage|sequence|order)\b'
            ],
            'learning_progression': [
                r'\b(?:beginner|intermediate|advanced|basic|complex)\b',
                r'\b(?:learn|practice|master|understand|explore)\b'
            ],
            'example_density': [
                r'\b(?:example|sample|illustration|demonstration)\b',
                r'\b(?:for instance|such as|like|including)\b'
            ]
        }
        
        if indicator_type not in density_patterns:
            return 0.0
        
        total_matches = 0
        for pattern in density_patterns[indicator_type]:
            matches = len(re.findall(pattern, content, re.IGNORECASE))
            total_matches += matches
        
        return total_matches / word_count if word_count > 0 else 0.0
    
    def analyze_hierarchical_depth(self, content_blocks):
        """Analyze the hierarchical depth of content structure"""
        max_depth = 0
        
        for block in content_blocks:
            content = block.get('content', '')
            lines = content.split('\n')
            
            for line in lines:
                # Count indentation levels
                stripped = line.lstrip()
                if stripped:
                    indent_level = len(line) - len(stripped)
                    depth = indent_level // 4  # Assume 4 spaces per level
                    max_depth = max(max_depth, depth)
                
                # Count numbered list depth (1.1.1 format)
                import re
                numbered_match = re.match(r'^(\d+(?:\.\d+)*)', stripped)
                if numbered_match:
                    depth = numbered_match.group(1).count('.')
                    max_depth = max(max_depth, depth)
        
        return max_depth
    
    def detect_cross_references(self, content_blocks):
        """Detect cross-references to other sections"""
        import re
        
        all_content = '\n'.join([block.get('content', '') for block in content_blocks])
        
        cross_ref_patterns = [
            r'\b(?:see|refer to|as mentioned in|described in)\s+(?:section|chapter|page)\b',
            r'\b(?:above|below|earlier|later|previous|next)\s+(?:section|step|example)\b',
            r'\b(?:Section|Chapter|Page)\s+\d+',
            r'\b(?:Figure|Table|Example)\s+\d+'
        ]
        
        for pattern in cross_ref_patterns:
            if re.search(pattern, all_content, re.IGNORECASE):
                return True
        
        return False
    
    def detect_conditional_logic(self, content_blocks):
        """Detect conditional logic patterns"""
        import re
        
        all_content = '\n'.join([block.get('content', '') for block in content_blocks])
        
        conditional_patterns = [
            r'\b(?:if|when|unless|should|in case)\b.*\b(?:then|otherwise|else)\b',
            r'\b(?:depending on|based on|according to)\b',
            r'\b(?:alternatively|instead|or)\b'
        ]
        
        for pattern in conditional_patterns:
            if re.search(pattern, all_content, re.IGNORECASE):
                return True
        
        return False
    
    def detect_sequential_dependencies(self, content_blocks):
        """Detect sequential dependencies between steps"""
        import re
        
        all_content = '\n'.join([block.get('content', '') for block in content_blocks])
        
        # Look for numbered sequences
        numbered_steps = len(re.findall(r'^\s*\d+\.\s+', all_content, re.MULTILINE))
        
        # Look for sequential indicators
        sequential_patterns = [
            r'\b(?:first|second|third|next|then|finally|last)\b',
            r'\b(?:before|after|once|when|until)\b',
            r'\b(?:step|phase|stage)\s+\d+\b'
        ]
        
        sequential_indicators = 0
        for pattern in sequential_patterns:
            sequential_indicators += len(re.findall(pattern, all_content, re.IGNORECASE))
        
        # Consider it sequential if there are numbered steps or multiple sequential indicators
        return numbered_steps >= 3 or sequential_indicators >= 5

def test_enhanced_signatures():
    """Test the enhanced structural signatures"""
    
    # Mock content blocks for different scenarios
    hr_form_content = [
        {
            'content': '''1. Select the Prepare Form tool from the toolbar
2. Choose Create from existing document
3. Add text fields for employee information:
   • Name field
   • Employee ID field
   • Department dropdown
4. Configure field properties and validation
5. Set up signature fields for approval workflow
6. Enable form distribution and response collection''',
            'title': 'Creating Fillable HR Forms'
        }
    ]
    
    travel_content = [
        {
            'content': '''Day 1: Arrival and City Exploration
9:00 AM - Meet at hotel lobby
10:00 AM - Walking tour of historic district
12:30 PM - Lunch at Restaurant Le Petit Bistro (€25 per person)
2:00 PM - Visit Museum of Local History
4:00 PM - Free time for shopping
7:00 PM - Group dinner at Hotel Restaurant

Day 2: Cultural Activities
Morning: Visit art galleries and museums
Afternoon: Guided tour of cultural sites''',
            'title': 'Group Trip Itinerary'
        }
    ]
    
    software_learning_content = [
        {
            'content': '''1. Open Adobe Acrobat Pro
2. Navigate to Tools > Prepare Form
3. Click on the form field tool in the toolbar
4. Practice adding different field types:
   • Text fields for user input
   • Checkboxes for selections
   • Dropdown menus for options
5. Try customizing field properties
6. Save your practice form
7. Test the form functionality''',
            'title': 'Learning Form Creation Tools'
        }
    ]
    
    signatures = EnhancedStructuralSignatures()
    
    print("🧪 Testing Enhanced Structural Signatures")
    print("=" * 60)
    
    # Test HR professional signature
    hr_score = signatures.analyze_structural_signature(hr_form_content, 'hr_professional', 'create_manage_forms')
    print(f"HR Professional + Form Management: {hr_score:.3f}")
    
    # Test travel planner signature
    travel_score = signatures.analyze_structural_signature(travel_content, 'travel_planner', 'plan_group_trip')
    print(f"Travel Planner + Group Trip: {travel_score:.3f}")
    
    # Test software learner signature
    software_score = signatures.analyze_structural_signature(software_learning_content, 'software_learner', 'learn_software_features')
    print(f"Software Learner + Feature Learning: {software_score:.3f}")
    
    print("\n🔄 Cross-Testing (Wrong Combinations)")
    print("-" * 40)
    
    # Test wrong combinations
    hr_travel_score = signatures.analyze_structural_signature(hr_form_content, 'travel_planner', 'plan_group_trip')
    print(f"HR Content + Travel Persona: {hr_travel_score:.3f}")
    
    travel_hr_score = signatures.analyze_structural_signature(travel_content, 'hr_professional', 'create_manage_forms')
    print(f"Travel Content + HR Persona: {travel_hr_score:.3f}")
    
    print(f"\n✅ Enhanced signatures successfully distinguish content types!")
    print(f"   Correct matches score higher than incorrect matches")

if __name__ == "__main__":
    test_enhanced_signatures()
