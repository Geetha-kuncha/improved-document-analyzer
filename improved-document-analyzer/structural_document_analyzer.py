import json
import os
import re
from datetime import datetime
from typing import List, Dict, Any, Tuple
import PyPDF2
from collections import Counter, defaultdict
import math

class StructuralDocumentAnalyzer:
    def __init__(self):
        # Structural analysis weights for relevance scoring
        self.relevance_weights = {
            'structural_complexity': 0.25,
            'information_density': 0.30,
            'content_organization': 0.20,
            'contextual_relevance': 0.25
        }
        
        # Structural patterns for different content types
        self.structural_patterns = {
            'list_structures': {
                'bullet_points': r'^\s*[•\-\*\+]\s+',
                'numbered_lists': r'^\s*\d+[\.\)]\s+',
                'lettered_lists': r'^\s*[a-z]\)\s+',
                'sub_lists': r'^\s*\d+\.\d+[\.\)]\s+'
            },
            'information_markers': {
                'key_value_pairs': r'^[^:\n]{3,50}:\s*[^:\n]{10,}',
                'measurements': r'\b\d+(?:\.\d+)?\s*(?:km|miles|hours?|days?|minutes?|euros?|€|$|£|%|meters?|feet)\b',
                'time_references': r'\b(?:\d{1,2}:\d{2}|\d{1,2}[ap]m|morning|afternoon|evening|night|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
                'locations': r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Street|St|Avenue|Ave|Road|Rd|Square|Place|Center|Centre|Museum|Hotel|Restaurant))\b',
                'contact_info': r'\b(?:www\.|http|@[\w.-]+|\+?\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4})\b',
                'prices': r'\b(?:€|$|£)\s*\d+(?:\.\d{2})?|\b\d+(?:\.\d{2})?\s*(?:euros?|dollars?|pounds?)\b'
            },
            'organizational_markers': {
                'headers': r'^[A-Z][A-Z\s]{5,}$',
                'section_breaks': r'^[A-Z][^:\n]{10,50}:\s*$',
                'emphasis': r'\b[A-Z]{2,}\b',
                'parenthetical': r'$$[^)]{5,50}$$'
            }
        }
        
        # Persona-job structural signatures
        self.persona_job_signatures = {
            'travel_planner': {
                'plan_itinerary': {
                    'required_structures': ['time_references', 'locations', 'numbered_lists'],
                    'preferred_content': ['activities', 'schedule', 'destinations'],
                    'organization_pattern': 'sequential_with_categories'
                },
                'find_accommodations': {
                    'required_structures': ['contact_info', 'prices', 'locations'],
                    'preferred_content': ['hotels', 'restaurants', 'booking'],
                    'organization_pattern': 'categorical_with_details'
                },
                'discover_activities': {
                    'required_structures': ['bullet_points', 'locations', 'time_references'],
                    'preferred_content': ['attractions', 'experiences', 'entertainment'],
                    'organization_pattern': 'categorical_listings'
                }
            },
            'cultural_explorer': {
                'explore_heritage': {
                    'required_structures': ['key_value_pairs', 'locations', 'headers'],
                    'preferred_content': ['history', 'culture', 'traditions'],
                    'organization_pattern': 'thematic_sections'
                },
                'visit_museums': {
                    'required_structures': ['locations', 'time_references', 'contact_info'],
                    'preferred_content': ['museums', 'galleries', 'exhibitions'],
                    'organization_pattern': 'location_based'
                }
            },
            'food_enthusiast': {
                'find_restaurants': {
                    'required_structures': ['locations', 'prices', 'contact_info'],
                    'preferred_content': ['restaurants', 'cuisine', 'dining'],
                    'organization_pattern': 'categorical_with_ratings'
                },
                'learn_cooking': {
                    'required_structures': ['numbered_lists', 'bullet_points', 'measurements'],
                    'preferred_content': ['recipes', 'ingredients', 'techniques'],
                    'organization_pattern': 'procedural'
                }
            }
        }

    def analyze_document_collection(self, pdf_paths: List[str], persona: str, job: str) -> Dict[str, Any]:
        """Main analysis function that processes document collection"""
        start_time = datetime.now()
        
        print(f"Analyzing {len(pdf_paths)} documents for persona: {persona}")
        print(f"Job to be done: {job}")
        
        # Extract content from all documents
        all_sections = []
        document_profiles = {}
        
        for pdf_path in pdf_paths:
            doc_sections, doc_profile = self.process_single_document(pdf_path)
            all_sections.extend(doc_sections)
            document_profiles[os.path.basename(pdf_path)] = doc_profile
        
        print(f"Extracted {len(all_sections)} sections from {len(pdf_paths)} documents")
        
        # Analyze collection structure
        collection_profile = self.analyze_collection_structure(all_sections, document_profiles)
        
        # Score sections based on persona-job fit
        scored_sections = self.score_sections_for_persona_job(all_sections, persona, job, collection_profile)
        
        # Select top sections ensuring document diversity
        selected_sections = self.select_diverse_sections(scored_sections, max_sections=5)
        
        # Generate subsection analysis
        subsection_analysis = self.generate_subsection_analysis(selected_sections[:3])
        
        # Prepare output
        result = {
            "metadata": {
                "input_documents": [os.path.basename(path) for path in pdf_paths],
                "persona": persona,
                "job_to_be_done": job,
                "processing_timestamp": start_time.isoformat()
            },
            "extracted_sections": [
                {
                    "document": section["document"],
                    "section_title": section["title"],
                    "importance_rank": i + 1,
                    "page_number": section["page_number"]
                }
                for i, section in enumerate(selected_sections)
            ],
            "subsection_analysis": subsection_analysis
        }
        
        return result

    def process_single_document(self, pdf_path: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Process a single PDF document and extract structured sections"""
        document_name = os.path.basename(pdf_path)
        sections = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    page_text = page.extract_text()
                    page_sections = self.extract_sections_from_page(page_text, page_num, document_name)
                    sections.extend(page_sections)
        
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
        
        # Analyze document structure profile
        doc_profile = self.analyze_document_profile(sections)
        
        return sections, doc_profile

    def extract_sections_from_page(self, page_text: str, page_num: int, document_name: str) -> List[Dict[str, Any]]:
        """Extract structured sections from a page using sliding window approach"""
        lines = [line.strip() for line in page_text.split('\n') if line.strip()]
        sections = []
        
        if len(lines) < 5:
            return sections
        
        # Use sliding window to identify content sections
        window_size = 12
        step_size = 6
        
        for i in range(0, len(lines) - window_size + 1, step_size):
            window_lines = lines[i:i + window_size]
            section = self.analyze_content_window(window_lines, i, page_num, document_name)
            
            if self.is_valid_section(section):
                sections.append(section)
        
        # Merge overlapping sections and filter by quality
        merged_sections = self.merge_overlapping_sections(sections)
        
        return merged_sections

    def analyze_content_window(self, lines: List[str], start_idx: int, page_num: int, document_name: str) -> Dict[str, Any]:
        """Analyze a window of content lines for structural patterns"""
        content_text = '\n'.join(lines)
        
        section = {
            'content': content_text,
            'lines': lines,
            'page_number': page_num,
            'document': document_name,
            'start_index': start_idx,
            'word_count': len(content_text.split()),
            'structural_elements': {},
            'title': '',
            'structural_score': 0.0,
            'information_density': 0.0,
            'organization_score': 0.0
        }
        
        # Analyze structural elements
        section['structural_elements'] = self.count_structural_elements(content_text)
        
        # Generate section title
        section['title'] = self.generate_section_title(lines)
        
        # Calculate structural scores
        section['structural_score'] = self.calculate_structural_score(section)
        section['information_density'] = self.calculate_information_density(content_text)
        section['organization_score'] = self.calculate_organization_score(section)
        
        return section

    def count_structural_elements(self, content: str) -> Dict[str, int]:
        """Count various structural elements in content"""
        elements = {}
        
        # Count list structures
        for element_type, patterns in self.structural_patterns['list_structures'].items():
            elements[element_type] = len(re.findall(patterns, content, re.MULTILINE))
        
        # Count information markers
        for element_type, pattern in self.structural_patterns['information_markers'].items():
            elements[element_type] = len(re.findall(pattern, content, re.MULTILINE | re.IGNORECASE))
        
        # Count organizational markers
        for element_type, pattern in self.structural_patterns['organizational_markers'].items():
            elements[element_type] = len(re.findall(pattern, content, re.MULTILINE))
        
        return elements

    def generate_section_title(self, lines: List[str]) -> str:
        """Generate a meaningful title for the section based on structural analysis"""
        # Look for the most informative line in the first few lines
        candidates = []
        
        for line in lines[:5]:
            line_clean = line.strip()
            
            if len(line_clean) < 8 or len(line_clean) > 100:
                continue
            
            score = 0
            
            # Prefer lines with proper nouns (locations, names)
            proper_nouns = len(re.findall(r'\b[A-Z][a-z]+\b', line_clean))
            score += proper_nouns * 2
            
            # Prefer lines with specific information
            has_numbers = bool(re.search(r'\b\d+\b', line_clean))
            if has_numbers:
                score += 1
            
            # Avoid list items as titles
            if re.match(r'^\s*[•\-\*\+\d+\.\)]\s+', line_clean):
                score -= 3
            
            # Prefer medium-length lines
            word_count = len(line_clean.split())
            if 3 <= word_count <= 12:
                score += 2
            
            # Prefer lines that look like headers
            if line_clean.isupper() or (line_clean[0].isupper() and ':' in line_clean):
                score += 1
            
            candidates.append((score, line_clean))
        
        if candidates:
            candidates.sort(reverse=True)
            best_title = candidates[0][1]
            
            # Clean up the title
            best_title = re.sub(r'^\d+[\.\)]\s*', '', best_title)
            best_title = re.sub(r'^[•\-\*\+]\s*', '', best_title)
            
            if len(best_title) > 80:
                best_title = best_title[:77] + "..."
            
            return best_title
        
        return "Content Section"

    def calculate_structural_score(self, section: Dict[str, Any]) -> float:
        """Calculate structural complexity score"""
        elements = section['structural_elements']
        
        # Weight different structural elements
        weights = {
            'bullet_points': 1.0,
            'numbered_lists': 1.2,
            'key_value_pairs': 1.1,
            'locations': 1.3,
            'contact_info': 1.4,
            'prices': 1.3,
            'time_references': 1.2,
            'measurements': 1.1
        }
        
        weighted_score = 0.0
        for element, count in elements.items():
            if count > 0:
                weight = weights.get(element, 1.0)
                weighted_score += count * weight
        
        # Normalize by word count
        if section['word_count'] > 0:
            return min(weighted_score / section['word_count'] * 10, 1.0)
        
        return 0.0

    def calculate_information_density(self, content: str) -> float:
        """Calculate information density based on specific data patterns"""
        if not content.strip():
            return 0.0
        
        word_count = len(content.split())
        if word_count == 0:
            return 0.0
        
        info_score = 0.0
        
        # High-value information patterns
        info_score += len(re.findall(r'\b\d+(?:\.\d+)?\s*(?:€|$|£|%|km|miles|hours?)\b', content)) * 3.0
        info_score += len(re.findall(r'\b\d{1,2}:\d{2}(?:\s*[ap]m)?\b', content)) * 2.5
        info_score += len(re.findall(r'\b(?:www\.|http|@[\w.-]+)\b', content)) * 2.0
        info_score += len(re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Street|Hotel|Restaurant|Museum))\b', content)) * 1.5
        
        return min(info_score / word_count * 5, 1.0)

    def calculate_organization_score(self, section: Dict[str, Any]) -> float:
        """Calculate how well-organized the content is"""
        elements = section['structural_elements']
        
        # Check for good organizational patterns
        organization_score = 0.0
        
        # Sequential organization (numbered lists)
        if elements.get('numbered_lists', 0) > 2:
            organization_score += 0.3
        
        # Categorical organization (bullet points with headers)
        if elements.get('bullet_points', 0) > 3 and elements.get('headers', 0) > 0:
            organization_score += 0.3
        
        # Information structure (key-value pairs)
        if elements.get('key_value_pairs', 0) > 2:
            organization_score += 0.2
        
        # Consistent formatting
        total_list_items = elements.get('bullet_points', 0) + elements.get('numbered_lists', 0)
        if total_list_items > 5:
            organization_score += 0.2
        
        return min(organization_score, 1.0)

    def is_valid_section(self, section: Dict[str, Any]) -> bool:
        """Check if a section meets minimum quality thresholds"""
        # Minimum word count
        if section['word_count'] < 30:
            return False
        
        # Must have some structural elements
        total_elements = sum(section['structural_elements'].values())
        if total_elements < 2:
            return False
        
        # Minimum structural score
        if section['structural_score'] < 0.1:
            return False
        
        return True

    def merge_overlapping_sections(self, sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Merge overlapping sections and keep the best ones"""
        if not sections:
            return []
        
        # Sort by start index
        sorted_sections = sorted(sections, key=lambda x: x['start_index'])
        merged = []
        
        current_section = sorted_sections[0]
        
        for next_section in sorted_sections[1:]:
            # Check for significant overlap
            current_end = current_section['start_index'] + len(current_section['lines'])
            overlap = max(0, current_end - next_section['start_index'])
            
            if overlap > len(current_section['lines']) * 0.4:  # 40% overlap
                # Keep the section with higher combined score
                current_combined = (current_section['structural_score'] + 
                                  current_section['information_density'] + 
                                  current_section['organization_score'])
                next_combined = (next_section['structural_score'] + 
                               next_section['information_density'] + 
                               next_section['organization_score'])
                
                if next_combined > current_combined:
                    current_section = next_section
            else:
                merged.append(current_section)
                current_section = next_section
        
        merged.append(current_section)
        
        # Filter by quality and limit number
        quality_sections = [section for section in merged if 
                          (section['structural_score'] + section['information_density']) > 0.3]
        
        # Sort by combined quality score
        quality_sections.sort(key=lambda x: (x['structural_score'] + 
                                           x['information_density'] + 
                                           x['organization_score']), reverse=True)
        
        return quality_sections[:15]  # Limit to top 15 per document

    def analyze_document_profile(self, sections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the overall structural profile of a document"""
        if not sections:
            return {}
        
        # Aggregate structural elements
        total_elements = defaultdict(int)
        for section in sections:
            for element, count in section['structural_elements'].items():
                total_elements[element] += count
        
        # Calculate averages
        avg_structural_score = sum(s['structural_score'] for s in sections) / len(sections)
        avg_info_density = sum(s['information_density'] for s in sections) / len(sections)
        avg_organization = sum(s['organization_score'] for s in sections) / len(sections)
        
        return {
            'section_count': len(sections),
            'structural_elements': dict(total_elements),
            'avg_structural_score': avg_structural_score,
            'avg_information_density': avg_info_density,
            'avg_organization_score': avg_organization,
            'document_type': self.classify_document_type(total_elements)
        }

    def classify_document_type(self, elements: Dict[str, int]) -> str:
        """Classify document type based on structural patterns"""
        # Travel guide indicators
        if (elements.get('locations', 0) > 20 and 
            elements.get('prices', 0) > 10 and 
            elements.get('contact_info', 0) > 5):
            return 'travel_guide'
        
        # Reference material indicators
        if (elements.get('bullet_points', 0) > 30 and 
            elements.get('key_value_pairs', 0) > 15):
            return 'reference_material'
        
        # Procedural content indicators
        if elements.get('numbered_lists', 0) > 20:
            return 'procedural_guide'
        
        return 'general_content'

    def analyze_collection_structure(self, all_sections: List[Dict[str, Any]], 
                                   document_profiles: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the structural characteristics of the entire collection"""
        
        # Aggregate all structural elements
        collection_elements = defaultdict(int)
        for section in all_sections:
            for element, count in section['structural_elements'].items():
                collection_elements[element] += count
        
        # Calculate collection-wide averages
        total_sections = len(all_sections)
        avg_structural_score = sum(s['structural_score'] for s in all_sections) / total_sections
        avg_info_density = sum(s['information_density'] for s in all_sections) / total_sections
        avg_organization = sum(s['organization_score'] for s in all_sections) / total_sections
        
        # Determine dominant document types
        doc_types = [profile.get('document_type', 'general') for profile in document_profiles.values()]
        dominant_type = Counter(doc_types).most_common(1)[0][0] if doc_types else 'general'
        
        return {
            'total_sections': total_sections,
            'collection_elements': dict(collection_elements),
            'avg_structural_score': avg_structural_score,
            'avg_information_density': avg_info_density,
            'avg_organization_score': avg_organization,
            'dominant_document_type': dominant_type,
            'document_diversity': len(set(doc_types)) / len(doc_types) if doc_types else 0
        }

    def score_sections_for_persona_job(self, sections: List[Dict[str, Any]], 
                                     persona: str, job: str, 
                                     collection_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Score sections based on how well they match the persona and job requirements"""
        
        # Normalize persona and job for matching
        persona_key = self.normalize_persona(persona)
        job_key = self.normalize_job(job)
        
        # Get structural signature for this persona-job combination
        signature = self.get_persona_job_signature(persona_key, job_key)
        
        scored_sections = []
        
        for section in sections:
            # Calculate base relevance score
            relevance_score = self.calculate_relevance_score(section, signature, collection_profile)
            
            # Add contextual relevance based on content
            contextual_score = self.calculate_contextual_relevance(section, persona, job)
            
            # Combine scores
            final_score = (relevance_score * 0.7) + (contextual_score * 0.3)
            
            section_copy = section.copy()
            section_copy['relevance_score'] = final_score
            section_copy['persona_job_match'] = relevance_score
            section_copy['contextual_match'] = contextual_score
            
            scored_sections.append(section_copy)
        
        # Sort by relevance score
        scored_sections.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return scored_sections

    def normalize_persona(self, persona: str) -> str:
        """Normalize persona string to match our signatures"""
        persona_lower = persona.lower()
        
        if any(word in persona_lower for word in ['travel', 'trip', 'planner', 'tourist']):
            return 'travel_planner'
        elif any(word in persona_lower for word in ['cultural', 'culture', 'explorer', 'heritage']):
            return 'cultural_explorer'
        elif any(word in persona_lower for word in ['food', 'culinary', 'cuisine', 'restaurant']):
            return 'food_enthusiast'
        
        return 'travel_planner'  # Default fallback

    def normalize_job(self, job: str) -> str:
        """Normalize job string to match our signatures"""
        job_lower = job.lower()
        
        if any(word in job_lower for word in ['plan', 'itinerary', 'schedule', 'trip']):
            return 'plan_itinerary'
        elif any(word in job_lower for word in ['accommodation', 'hotel', 'restaurant', 'dining']):
            return 'find_accommodations'
        elif any(word in job_lower for word in ['activity', 'activities', 'things to do', 'attractions']):
            return 'discover_activities'
        elif any(word in job_lower for word in ['heritage', 'history', 'culture', 'museum']):
            return 'explore_heritage'
        elif any(word in job_lower for word in ['cooking', 'recipe', 'culinary', 'learn']):
            return 'learn_cooking'
        
        return 'plan_itinerary'  # Default fallback

    def get_persona_job_signature(self, persona_key: str, job_key: str) -> Dict[str, Any]:
        """Get the structural signature for a persona-job combination"""
        if persona_key in self.persona_job_signatures:
            if job_key in self.persona_job_signatures[persona_key]:
                return self.persona_job_signatures[persona_key][job_key]
            else:
                # Return first available job for this persona
                jobs = list(self.persona_job_signatures[persona_key].keys())
                return self.persona_job_signatures[persona_key][jobs[0]]
        
        # Default signature
        return {
            'required_structures': ['bullet_points', 'locations'],
            'preferred_content': ['information', 'details'],
            'organization_pattern': 'categorical_listings'
        }

    def calculate_relevance_score(self, section: Dict[str, Any], 
                                signature: Dict[str, Any], 
                                collection_profile: Dict[str, Any]) -> float:
        """Calculate how well a section matches the structural signature"""
        
        elements = section['structural_elements']
        
        # Check required structures
        structure_score = 0.0
        required_structures = signature.get('required_structures', [])
        
        for structure in required_structures:
            if elements.get(structure, 0) > 0:
                structure_score += 1.0
        
        if required_structures:
            structure_score /= len(required_structures)
        
        # Weight by section quality scores
        quality_score = (section['structural_score'] * 0.4 + 
                        section['information_density'] * 0.4 + 
                        section['organization_score'] * 0.2)
        
        # Combine scores
        relevance_score = (structure_score * 0.6) + (quality_score * 0.4)
        
        return min(relevance_score, 1.0)

    def calculate_contextual_relevance(self, section: Dict[str, Any], 
                                     persona: str, job: str) -> float:
        """Calculate contextual relevance based on content analysis"""
        content = section['content'].lower()
        
        # Define contextual keywords for different persona-job combinations
        context_keywords = {
            'travel_planner': {
                'plan': ['itinerary', 'schedule', 'days', 'trip', 'visit', 'travel', 'plan'],
                'accommodations': ['hotel', 'restaurant', 'accommodation', 'stay', 'dining', 'eat'],
                'activities': ['activities', 'attractions', 'things to do', 'entertainment', 'experience']
            },
            'cultural_explorer': {
                'heritage': ['history', 'culture', 'heritage', 'tradition', 'historical', 'cultural'],
                'museums': ['museum', 'gallery', 'exhibition', 'art', 'collection']
            },
            'food_enthusiast': {
                'restaurants': ['restaurant', 'cuisine', 'dining', 'food', 'culinary'],
                'cooking': ['recipe', 'cooking', 'ingredients', 'preparation', 'chef']
            }
        }
        
        # Get relevant keywords
        persona_key = self.normalize_persona(persona)
        job_key = self.normalize_job(job)
        
        relevant_keywords = []
        if persona_key in context_keywords:
            for job_keywords in context_keywords[persona_key].values():
                relevant_keywords.extend(job_keywords)
        
        # Count keyword matches
        keyword_matches = sum(1 for keyword in relevant_keywords if keyword in content)
        
        # Normalize by content length and keyword count
        if relevant_keywords and section['word_count'] > 0:
            contextual_score = keyword_matches / len(relevant_keywords)
            return min(contextual_score, 1.0)
        
        return 0.0

    def select_diverse_sections(self, scored_sections: List[Dict[str, Any]], 
                              max_sections: int = 5) -> List[Dict[str, Any]]:
        """Select top sections while ensuring document diversity"""
        
        selected = []
        document_counts = defaultdict(int)
        max_per_document = max(2, max_sections // 3)  # Allow at most 1/3 from same document
        
        for section in scored_sections:
            doc_name = section['document']
            
            if (len(selected) < max_sections and 
                document_counts[doc_name] < max_per_document):
                
                selected.append(section)
                document_counts[doc_name] += 1
        
        return selected

    def generate_subsection_analysis(self, top_sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate refined subsection analysis for top sections"""
        
        subsection_analysis = []
        
        for section in top_sections:
            # Extract the most relevant part of the content
            refined_text = self.extract_refined_text(section)
            
            subsection_analysis.append({
                "document": section["document"],
                "refined_text": refined_text,
                "page_number": section["page_number"]
            })
        
        return subsection_analysis

    def extract_refined_text(self, section: Dict[str, Any]) -> str:
        """Extract the most relevant portion of a section's content"""
        content = section['content']
        lines = section['lines']
        
        # If content is short enough, return as is
        if len(content) <= 500:
            return content
        
        # Find the most information-dense part
        best_start = 0
        best_score = 0
        window_size = 8  # lines
        
        for i in range(len(lines) - window_size + 1):
            window_lines = lines[i:i + window_size]
            window_text = '\n'.join(window_lines)
            
            # Score this window
            elements = self.count_structural_elements(window_text)
            info_density = self.calculate_information_density(window_text)
            
            # Prefer windows with more structural elements and information
            score = sum(elements.values()) + (info_density * 10)
            
            if score > best_score:
                best_score = score
                best_start = i
        
        # Extract the best window
        best_lines = lines[best_start:best_start + window_size]
        refined_text = '\n'.join(best_lines)
        
        # Truncate if still too long
        if len(refined_text) > 500:
            refined_text = refined_text[:497] + "..."
        
        return refined_text

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Structural Document Analyzer for Persona-Driven Intelligence')
    parser.add_argument('--input_dir', required=True, help='Directory containing PDF files')
    parser.add_argument('--persona', required=True, help='User persona description')
    parser.add_argument('--job', required=True, help='Job to be done description')
    parser.add_argument('--output', default='analysis_results.json', help='Output JSON file')
    
    args = parser.parse_args()
    
    # Find PDF files
    pdf_files = []
    for file in os.listdir(args.input_dir):
        if file.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(args.input_dir, file))
    
    if not pdf_files:
        print("No PDF files found in input directory")
        return
    
    print(f"Found {len(pdf_files)} PDF files")
    print(f"Persona: {args.persona}")
    print(f"Job: {args.job}")
    
    # Initialize analyzer
    analyzer = StructuralDocumentAnalyzer()
    
    # Process documents
    result = analyzer.analyze_document_collection(pdf_files, args.persona, args.job)
    
    # Save results
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\nAnalysis complete! Results saved to {args.output}")
    print(f"Selected {len(result['extracted_sections'])} sections")
    print(f"Generated {len(result['subsection_analysis'])} subsection analyses")
    
    # Print summary
    print("\n=== SELECTED SECTIONS ===")
    for section in result['extracted_sections']:
        print(f"{section['importance_rank']}. {section['section_title']}")
        print(f"   Document: {section['document']} (Page {section['page_number']})")

if __name__ == "__main__":
    main()
