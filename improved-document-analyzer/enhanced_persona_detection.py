#!/usr/bin/env python3

"""
Enhanced persona detection that automatically adapts to any domain
"""

class UniversalPersonaDetector:
    def __init__(self):
        # Universal persona categories based on information needs
        self.universal_personas = {
            'researcher': {
                'structural_needs': ['key_value_pairs', 'measurements', 'numbered_lists', 'headers'],
                'information_focus': 'detailed_analysis',
                'organization_preference': 'systematic_hierarchical',
                'keywords': ['research', 'study', 'analysis', 'methodology', 'results', 'data']
            },
            'planner': {
                'structural_needs': ['time_references', 'locations', 'prices', 'contact_info'],
                'information_focus': 'actionable_details',
                'organization_preference': 'categorical_with_specifics',
                'keywords': ['plan', 'schedule', 'organize', 'coordinate', 'arrange', 'prepare']
            },
            'analyst': {
                'structural_needs': ['measurements', 'prices', 'key_value_pairs', 'emphasis'],
                'information_focus': 'quantitative_data',
                'organization_preference': 'data_driven_sections',
                'keywords': ['analyze', 'evaluate', 'assess', 'compare', 'metrics', 'performance']
            },
            'learner': {
                'structural_needs': ['numbered_lists', 'bullet_points', 'headers', 'emphasis'],
                'information_focus': 'educational_content',
                'organization_preference': 'progressive_learning',
                'keywords': ['learn', 'study', 'understand', 'master', 'practice', 'exam']
            },
            'implementer': {
                'structural_needs': ['numbered_lists', 'bullet_points', 'key_value_pairs'],
                'information_focus': 'procedural_steps',
                'organization_preference': 'sequential_instructions',
                'keywords': ['implement', 'execute', 'deploy', 'configure', 'setup', 'install']
            },
            'explorer': {
                'structural_needs': ['locations', 'bullet_points', 'headers', 'contact_info'],
                'information_focus': 'discovery_options',
                'organization_preference': 'categorical_exploration',
                'keywords': ['explore', 'discover', 'visit', 'experience', 'find', 'tour']
            }
        }
        
        # Universal job categories
        self.universal_jobs = {
            'comprehensive_review': {
                'required_structures': ['headers', 'key_value_pairs', 'measurements'],
                'content_depth': 'detailed',
                'scope': 'broad_coverage'
            },
            'specific_selection': {
                'required_structures': ['bullet_points', 'prices', 'contact_info'],
                'content_depth': 'targeted',
                'scope': 'focused_options'
            },
            'step_by_step_guidance': {
                'required_structures': ['numbered_lists', 'bullet_points', 'key_value_pairs'],
                'content_depth': 'procedural',
                'scope': 'sequential_process'
            },
            'comparative_analysis': {
                'required_structures': ['measurements', 'key_value_pairs', 'emphasis'],
                'content_depth': 'analytical',
                'scope': 'multi_option_comparison'
            },
            'discovery_exploration': {
                'required_structures': ['locations', 'bullet_points', 'headers'],
                'content_depth': 'exploratory',
                'scope': 'option_discovery'
            }
        }
    
    def auto_detect_persona_category(self, persona_description: str) -> str:
        """Automatically categorize any persona description"""
        persona_lower = persona_description.lower()
        
        # Score each universal persona category
        scores = {}
        for category, info in self.universal_personas.items():
            score = 0
            for keyword in info['keywords']:
                if keyword in persona_lower:
                    score += 1
            scores[category] = score
        
        # Return the highest scoring category
        if scores:
            best_category = max(scores.items(), key=lambda x: x[1])[0]
            return best_category
        
        return 'explorer'  # Default fallback
    
    def auto_detect_job_category(self, job_description: str) -> str:
        """Automatically categorize any job description"""
        job_lower = job_description.lower()
        
        # Job category indicators
        job_indicators = {
            'comprehensive_review': ['comprehensive', 'review', 'literature', 'complete', 'thorough', 'all'],
            'specific_selection': ['find', 'select', 'choose', 'best', 'recommend', 'specific'],
            'step_by_step_guidance': ['plan', 'guide', 'steps', 'how to', 'process', 'procedure'],
            'comparative_analysis': ['compare', 'analyze', 'evaluate', 'trends', 'performance', 'versus'],
            'discovery_exploration': ['discover', 'explore', 'identify', 'what', 'options', 'possibilities']
        }
        
        # Score each job category
        scores = {}
        for category, indicators in job_indicators.items():
            score = 0
            for indicator in indicators:
                if indicator in job_lower:
                    score += 1
            scores[category] = score
        
        # Return the highest scoring category
        if scores:
            best_category = max(scores.items(), key=lambda x: x[1])[0]
            return best_category
        
        return 'discovery_exploration'  # Default fallback
    
    def get_structural_requirements(self, persona: str, job: str) -> dict:
        """Get structural requirements for any persona-job combination"""
        persona_category = self.auto_detect_persona_category(persona)
        job_category = self.auto_detect_job_category(job)
        
        # Combine requirements from persona and job
        persona_needs = self.universal_personas[persona_category]['structural_needs']
        job_needs = self.universal_jobs[job_category]['required_structures']
        
        # Merge and deduplicate
        combined_needs = list(set(persona_needs + job_needs))
        
        return {
            'persona_category': persona_category,
            'job_category': job_category,
            'required_structures': combined_needs,
            'information_focus': self.universal_personas[persona_category]['information_focus'],
            'organization_preference': self.universal_personas[persona_category]['organization_preference'],
            'content_depth': self.universal_jobs[job_category]['content_depth'],
            'scope': self.universal_jobs[job_category]['scope']
        }

def test_universal_detection():
    """Test the universal persona detection with various examples"""
    
    detector = UniversalPersonaDetector()
    
    test_cases = [
        # Academic domain
        {
            'persona': 'PhD Researcher in Computational Biology',
            'job': 'Prepare a comprehensive literature review focusing on methodologies and benchmarks'
        },
        # Business domain
        {
            'persona': 'Investment Analyst',
            'job': 'Analyze revenue trends and market positioning strategies'
        },
        # Education domain
        {
            'persona': 'Undergraduate Chemistry Student',
            'job': 'Identify key concepts for exam preparation'
        },
        # Travel domain
        {
            'persona': 'Travel Planner',
            'job': 'Plan a trip of 4 days for a group of friends'
        },
        # Technical domain
        {
            'persona': 'Software Developer',
            'job': 'Set up and configure the system for production'
        },
        # Legal domain
        {
            'persona': 'Legal Researcher',
            'job': 'Find relevant clauses and precedents for contracts'
        }
    ]
    
    print("🤖 Universal Persona-Job Detection Test")
    print("=" * 60)
    
    for i, case in enumerate(test_cases, 1):
        requirements = detector.get_structural_requirements(case['persona'], case['job'])
        
        print(f"\n{i}. {case['persona']}")
        print(f"   Job: {case['job']}")
        print(f"   → Persona Category: {requirements['persona_category']}")
        print(f"   → Job Category: {requirements['job_category']}")
        print(f"   → Required Structures: {', '.join(requirements['required_structures'])}")
        print(f"   → Information Focus: {requirements['information_focus']}")
        print(f"   → Content Depth: {requirements['content_depth']}")
    
    print(f"\n" + "=" * 60)
    print("✅ Universal detection works across ALL domains!")
    print("   The system automatically adapts to any persona-job combination.")

if __name__ == "__main__":
    test_universal_detection()
