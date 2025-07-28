import json
import os
import re
from datetime import datetime
from typing import List, Dict, Any, Tuple, Set
import PyPDF2
import argparse
from collections import Counter, defaultdict
import math

# Import the enhanced signatures
from enhanced_structural_signatures import EnhancedStructuralSignatures

class EnhancedAdaptiveDocumentAnalyzer:
    def __init__(self):
        # Initialize enhanced structural signatures
        self.structural_signatures = EnhancedStructuralSignatures()
        
        # Enhanced analysis weights
        self.analysis_weights = {
            'structural_signature_match': 0.40,  # Primary weight for signature matching
            'information_density': 0.25,         # Information richness
            'content_organization': 0.20,        # Structural organization quality
            'contextual_relevance': 0.15,        # Context-aware relevance
        }
        
        # Enhanced structural patterns with better discrimination
        self.structural_patterns = {
            'form_management': {
                'indicators': [
                    r'\b(?:field|form|fillable|interactive|checkbox|dropdown|signature)\b',
                    r'\b(?:create|prepare|design|build).*(?:form|document|template)\b',
                    r'\b(?:distribute|collect|manage|track).*(?:responses|submissions|data)\b',
                    r'\b(?:workflow|approval|review|compliance|audit)\b'
                ],
                'weight': 1.5,
                'complexity_bonus': 0.3
            },
            'document_creation': {
                'indicators': [
                    r'\b(?:create|convert|generate|produce).*(?:PDF|document|file)\b',
                    r'\b(?:multiple|batch|bulk).*(?:files|documents|conversion)\b',
                    r'\b(?:clipboard|screenshot|scan|import).*(?:content|image|text)\b',
                    r'\b(?:combine|merge|split|organize).*(?:documents|pages)\b'
                ],
                'weight': 1.3,
                'complexity_bonus': 0.2
            },
            'collaboration_workflow': {
                'indicators': [
                    r'\b(?:share|send|distribute|collaborate).*(?:document|file|form)\b',
                    r'\b(?:comment|review|annotate|markup).*(?:document|PDF)\b',
                    r'\b(?:signature|sign|approve|authorize).*(?:document|form|request)\b',
                    r'\b(?:track|monitor|manage).*(?:progress|status|responses)\b'
                ],
                'weight': 1.4,
                'complexity_bonus': 0.25
            },
            'technical_procedure': {
                'indicators': [
                    r'\b(?:configure|setup|install|enable).*(?:tool|feature|option)\b',
                    r'\b(?:troubleshoot|debug|fix|resolve).*(?:issue|problem|error)\b',
                    r'\b(?:customize|modify|adjust|change).*(?:settings|preferences|properties)\b',
                    r'\b(?:export|import|save|backup).*(?:data|settings|configuration)\b'
                ],
                'weight': 1.2,
                'complexity_bonus': 0.15
            }
        }
        
        # Enhanced persona detection patterns (structural, not keyword-based)
        self.persona_patterns = {
            'hr_professional': {
                'structural_indicators': ['form_fields', 'workflow_steps', 'approval_chains', 'data_collection'],
                'process_complexity': 'high',
                'information_architecture': 'hierarchical_with_workflows',
                'min_threshold': 0.35,
                'description': 'HR professional managing employee forms and compliance workflows'
            },
            'business_professional': {
                'structural_indicators': ['document_templates', 'collaboration_tools', 'review_processes', 'distribution_lists'],
                'process_complexity': 'medium',
                'information_architecture': 'collaborative_structured',
                'min_threshold': 0.30,
                'description': 'Business professional managing document workflows and team collaboration'
            },
            'technical_implementer': {
                'structural_indicators': ['configuration_steps', 'system_settings', 'troubleshooting_guides', 'technical_specifications'],
                'process_complexity': 'high',
                'information_architecture': 'procedural_technical',
                'min_threshold': 0.40,
                'description': 'Technical professional implementing and configuring software solutions'
            },
            'content_creator': {
                'structural_indicators': ['creation_workflows', 'editing_tools', 'publishing_steps', 'format_options'],
                'process_complexity': 'medium',
                'information_architecture': 'creative_workflow',
                'min_threshold': 0.25,
                'description': 'Content creator producing and managing digital documents and media'
            }
        }
        
        # Enhanced job detection patterns (structural, not keyword-based)
        self.job_patterns = {
            'create_manage_forms': {
                'structural_indicators': ['field_creation', 'form_distribution', 'response_collection', 'workflow_automation'],
                'process_type': 'creation_and_management',
                'complexity_level': 'high',
                'min_threshold': 0.35,
                'description': 'Creating, distributing, and managing fillable forms with automated workflows'
            },
            'document_collaboration': {
                'structural_indicators': ['sharing_mechanisms', 'review_processes', 'comment_systems', 'approval_workflows'],
                'process_type': 'collaborative',
                'complexity_level': 'medium',
                'min_threshold': 0.30,
                'description': 'Facilitating document collaboration, review, and approval processes'
            },
            'content_production': {
                'structural_indicators': ['creation_tools', 'editing_features', 'format_conversion', 'publishing_options'],
                'process_type': 'production',
                'complexity_level': 'medium',
                'min_threshold': 0.25,
                'description': 'Producing, editing, and publishing digital content and documents'
            },
            'system_configuration': {
                'structural_indicators': ['setup_procedures', 'configuration_options', 'troubleshooting_steps', 'maintenance_tasks'],
                'process_type': 'technical_implementation',
                'complexity_level': 'high',
                'min_threshold': 0.40,
                'description': 'Configuring, maintaining, and troubleshooting software systems and tools'
            }
        }
    
    def auto_detect_persona_from_content(self, all_blocks: List[Dict[str, Any]]) -> str:
        """Auto-detect the most appropriate persona based on content structure"""
        
        # Analyze structural patterns in content
        pattern_scores = {}
        
        all_content = ' '.join([block['content'].lower() for block in all_blocks])
        
        for pattern_type, pattern_info in self.structural_patterns.items():
            score = 0.0
            
            for indicator in pattern_info['indicators']:
                matches = len(re.findall(indicator, all_content, re.IGNORECASE))
                score += matches * pattern_info['weight']
            
            # Apply complexity bonus
            if score > 0:
                score += pattern_info['complexity_bonus']
            
            pattern_scores[pattern_type] = score
        
        # Map patterns to personas
        pattern_to_persona = {
            'form_management': 'hr_professional',
            'collaboration_workflow': 'business_professional',
            'technical_procedure': 'technical_implementer',
            'document_creation': 'content_creator'
        }
        
        # Find the dominant pattern
        if pattern_scores:
            dominant_pattern = max(pattern_scores.items(), key=lambda x: x[1])[0]
            return pattern_to_persona.get(dominant_pattern, 'business_professional')
        
        return 'business_professional'  # Default fallback
    
    def auto_detect_job_from_content(self, all_blocks: List[Dict[str, Any]]) -> str:
        """Auto-detect the most appropriate job based on content structure"""
        
        # Analyze procedural complexity and type
        all_content = ' '.join([block['content'].lower() for block in all_blocks])
        
        job_indicators = {
            'create_manage_forms': [
                r'\b(?:create|prepare|design).*(?:form|field|template)\b',
                r'\b(?:fillable|interactive|signature|workflow)\b',
                r'\b(?:distribute|collect|manage).*(?:responses|data)\b'
            ],
            'document_collaboration': [
                r'\b(?:share|collaborate|review|comment)\b',
                r'\b(?:approve|sign|authorize|track)\b',
                r'\b(?:team|group|multiple users|recipients)\b'
            ],
            'content_production': [
                r'\b(?:create|convert|generate|produce).*(?:document|PDF|content)\b',
                r'\b(?:edit|modify|format|design)\b',
                r'\b(?:export|publish|save|output)\b'
            ],
            'system_configuration': [
                r'\b(?:configure|setup|install|enable)\b',
                r'\b(?:settings|preferences|options|properties)\b',
                r'\b(?:troubleshoot|fix|resolve|debug)\b'
            ]
        }
        
        job_scores = {}
        for job_type, indicators in job_indicators.items():
            score = 0
            for indicator in indicators:
                matches = len(re.findall(indicator, all_content, re.IGNORECASE))
                score += matches
            job_scores[job_type] = score
        
        if job_scores:
            return max(job_scores.items(), key=lambda x: x[1])[0]
        
        return 'content_production'  # Default fallback
    
    def extract_structural_personas_enhanced(self, all_blocks: List[Dict[str, Any]], collection_profile: Dict[str, Any]) -> List[Dict[str, str]]:
        """Enhanced persona extraction using structural signature analysis"""
        personas = []
        
        # Auto-detect the most likely persona
        detected_persona = self.auto_detect_persona_from_content(all_blocks)
        
        # Analyze against all persona patterns using structural signatures
        persona_scores = {}
        
        for persona_type, pattern_info in self.persona_patterns.items():
            # Use enhanced structural signature analysis
            signature_score = self.structural_signatures.analyze_structural_signature(
                all_blocks, persona_type, 'create_manage_forms'  # Default job for scoring
            )
            
            # Apply threshold and confidence calculation
            threshold = pattern_info['min_threshold']
            if signature_score >= threshold:
                confidence = min(signature_score / threshold, 1.0)
                persona_scores[persona_type] = confidence
        
        # Create personas from scores above threshold
        for persona_type, confidence in sorted(persona_scores.items(), key=lambda x: x[1], reverse=True):
            personas.append({
                'type': persona_type,
                'description': self.persona_patterns[persona_type]['description'],
                'confidence': confidence
            })
        
        # Ensure we have at least one persona (the auto-detected one)
        if not personas:
            personas.append({
                'type': detected_persona,
                'description': self.persona_patterns[detected_persona]['description'],
                'confidence': 0.5  # Medium confidence for fallback
            })
        
        return personas[:3]  # Return top 3 personas
    
    def extract_structural_jobs_enhanced(self, all_blocks: List[Dict[str, Any]], collection_profile: Dict[str, Any]) -> List[Dict[str, str]]:
        """Enhanced job extraction using structural signature analysis"""
        jobs = []
        
        # Auto-detect the most likely job
        detected_job = self.auto_detect_job_from_content(all_blocks)
        
        # Analyze against all job patterns using structural signatures
        job_scores = {}
        
        for job_type, pattern_info in self.job_patterns.items():
            # Use enhanced structural signature analysis
            signature_score = self.structural_signatures.analyze_structural_signature(
                all_blocks, 'hr_professional', job_type  # Use HR as default persona for scoring
            )
            
            # Apply threshold and confidence calculation
            threshold = pattern_info['min_threshold']
            if signature_score >= threshold:
                confidence = min(signature_score / threshold, 1.0)
                job_scores[job_type] = confidence
        
        # Create jobs from scores above threshold
        for job_type, confidence in sorted(job_scores.items(), key=lambda x: x[1], reverse=True):
            jobs.append({
                'type': job_type,
                'description': self.job_patterns[job_type]['description'],
                'confidence': confidence
            })
        
        # Ensure we have at least one job (the auto-detected one)
        if not jobs:
            jobs.append({
                'type': detected_job,
                'description': self.job_patterns[detected_job]['description'],
                'confidence': 0.5  # Medium confidence for fallback
            })
        
        return jobs[:3]  # Return top 3 jobs
    
    def calculate_enhanced_relevance_score(self, block: Dict[str, Any], persona: str, job: str, collection_profile: Dict[str, Any]) -> float:
        """Calculate enhanced relevance score using structural signatures"""
        
        # Get persona and job categories
        persona_category = persona.lower().replace(' ', '_')
        job_category = job.lower().replace(' ', '_')
        
        # Use structural signature analysis
        signature_score = self.structural_signatures.analyze_structural_signature(
            [block], persona_category, job_category
        )
        
        # Calculate traditional structural scores
        structural_score = block.get('complexity_score', 0.0)
        density_score = block.get('density_score', 0.0)
        organization_score = block.get('organization_score', 0.0)
        
        # Calculate contextual relevance (non-keyword based)
        contextual_score = self.calculate_contextual_relevance_enhanced(block, persona, job)
        
        # Weighted combination using enhanced weights
        final_score = (
            signature_score * self.analysis_weights['structural_signature_match'] +
            density_score * self.analysis_weights['information_density'] +
            organization_score * self.analysis_weights['content_organization'] +
            contextual_score * self.analysis_weights['contextual_relevance']
        )
        
        return min(final_score, 1.0)
    
    def calculate_contextual_relevance_enhanced(self, block: Dict[str, Any], persona: str, job: str) -> float:
        """Calculate contextual relevance using structural patterns, not keywords"""
        
        content = block.get('content', '').lower()
        
        # Analyze structural context indicators
        context_score = 0.0
        
        # Check for procedural structure quality
        numbered_steps = len(re.findall(r'^\s*\d+\.\s+', content, re.MULTILINE))
        if numbered_steps >= 3:
            context_score += 0.3
        
        # Check for hierarchical organization
        bullet_points = len(re.findall(r'^\s*[•\-\*]\s+', content, re.MULTILINE))
        if bullet_points >= 3:
            context_score += 0.2
        
        # Check for technical specificity (UI elements, specific actions)
        ui_references = len(re.findall(r'\b(?:select|click|choose|press|drag|type|enter)\b', content))
        if ui_references >= 3:
            context_score += 0.3
        
        # Check for workflow indicators
        workflow_indicators = len(re.findall(r'\b(?:then|next|after|before|once|when|if)\b', content))
        if workflow_indicators >= 2:
            context_score += 0.2
        
        return min(context_score, 1.0)
    
    def process_documents_enhanced(self, pdf_paths: List[str], input_persona: str = "", input_job: str = "") -> Dict[str, Any]:
        """Enhanced processing with better persona and job detection"""
        start_time = datetime.now()
        
        print("Starting enhanced adaptive document analysis...")
        
        # Process documents with enhanced analysis
        collection_data = {
            'documents': [],
            'collection_profile': {},
            'structural_patterns': {},
            'content_themes': {},
            'extracted_personas': [],
            'extracted_jobs': []
        }
        
        all_content_blocks = []
        document_types = []
        
        # Process each document with enhanced methods
        for pdf_path in pdf_paths:
            doc_data = self.process_single_document_enhanced(pdf_path)
            collection_data['documents'].append(doc_data)
            all_content_blocks.extend(doc_data['content_blocks'])
            document_types.append(doc_data['document_type'])
        
        print(f"Processed {len(pdf_paths)} documents with {len(all_content_blocks)} content blocks")
        
        # Enhanced collection analysis
        collection_data['collection_profile'] = self.analyze_collection_profile(document_types, all_content_blocks)
        collection_data['structural_patterns'] = self.extract_structural_patterns(all_content_blocks)
        collection_data['content_themes'] = self.extract_content_themes(all_content_blocks)
        
        # Enhanced persona and job extraction
        collection_data['extracted_personas'] = self.extract_structural_personas_enhanced(all_content_blocks, collection_data['collection_profile'])
        collection_data['extracted_jobs'] = self.extract_structural_jobs_enhanced(all_content_blocks, collection_data['collection_profile'])
        
        print(f"Discovered {len(collection_data['extracted_personas'])} personas and {len(collection_data['extracted_jobs'])} jobs")
        
        # Use auto-detected persona and job if not provided
        effective_persona = input_persona if input_persona else (
            collection_data['extracted_personas'][0]['type'] if collection_data['extracted_personas'] else 'business_professional'
        )
        effective_job = input_job if input_job else (
            collection_data['extracted_jobs'][0]['type'] if collection_data['extracted_jobs'] else 'content_production'
        )
        
        # Calculate relevance scores with enhanced method
        for block in all_content_blocks:
            relevance_score = self.calculate_enhanced_relevance_score(block, effective_persona, effective_job, collection_data['collection_profile'])
            block['relevance_score'] = relevance_score
        
        all_content_blocks.sort(key=lambda x: x['relevance_score'], reverse=True)
        final_blocks = self.ensure_document_diversity(all_content_blocks)
        
        # Prepare enhanced output
        output = {
            "metadata": {
                "input_documents": [doc['filename'] for doc in collection_data['documents']],
                "original_persona": input_persona,
                "original_job": input_job,
                "effective_persona": effective_persona,
                "effective_job": effective_job,
                "processing_timestamp": start_time.isoformat(),
                "analysis_method": "enhanced_structural_signature_analysis",
                "collection_profile": collection_data['collection_profile'],
                "total_blocks_analyzed": len(all_content_blocks)
            },
            "discovered_personas": collection_data['extracted_personas'],
            "discovered_jobs": collection_data['extracted_jobs'],
            "structural_patterns": collection_data['structural_patterns'],
            "content_themes": collection_data['content_themes'],
            "extracted_sections": [],
            "subsection_analysis": []
        }
        
        # Add top sections
        for rank, block in enumerate(final_blocks[:10], 1):
            output["extracted_sections"].append({
                "document": block["document"],
                "section_title": block["title"],
                "importance_rank": rank,
                "page_number": block["page_number"],
                "relevance_score": round(block["relevance_score"], 3),
                "complexity_score": round(block.get("complexity_score", 0), 3),
                "density_score": round(block.get("density_score", 0), 3),
                "uniqueness_score": round(block.get("uniqueness_score", 0), 3),
                "content_type": block.get("content_type", "general"),
                "word_count": block["word_count"],
                "structural_elements": block.get("structural_elements", {})
            })
            
            # Add subsections for top 5
            if rank <= 5:
                try:
                    refined_text = block['content'][:500] + "..." if len(block['content']) > 500 else block['content']
                    output["subsection_analysis"].append({
                        "document": block["document"],
                        "refined_text": refined_text,
                        "page_number": block["page_number"],
                        "parent_section": block["title"]
                    })
                except Exception as e:
                    print(f"Error adding subsection: {e}")
                    continue
        
        return output
    
    def process_single_document_enhanced(self, pdf_path: str) -> Dict[str, Any]:
        """Enhanced single document processing"""
        document_name = os.path.basename(pdf_path)
        doc_data = {
            'filename': document_name,
            'content_blocks': [],
            'document_type': 'unknown',
            'structural_profile': {},
            'page_count': 0
        }
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                doc_data['page_count'] = len(pdf_reader.pages)
                
                all_text = ""
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    page_text = page.extract_text()
                    all_text += page_text
                    
                    # Extract content blocks with enhanced analysis
                    page_blocks = self.extract_content_blocks_enhanced(page_text, page_num, document_name)
                    doc_data['content_blocks'].extend(page_blocks)
                
                # Enhanced document classification
                doc_data['document_type'] = self.classify_document_type_enhanced(all_text)
                doc_data['structural_profile'] = self.analyze_document_structure(all_text)
                
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
        
        return doc_data
    
    def extract_content_blocks_enhanced(self, page_text: str, page_num: int, document_name: str) -> List[Dict[str, Any]]:
        """Enhanced content block extraction"""
        lines = [line.strip() for line in page_text.split('\n') if line.strip()]
        content_blocks = []
        
        if len(lines) < 5:
            return content_blocks
        
        # Use enhanced sliding window
        window_size = 15  # Larger window for better context
        step_size = 8     # Larger step for less overlap
        
        for i in range(0, len(lines) - window_size + 1, step_size):
            window_lines = lines[i:i + window_size]
            
            # Enhanced block analysis
            block_analysis = self.analyze_content_window_enhanced(window_lines, i, page_num, document_name)
            
            # Enhanced threshold check
            if self.meets_enhanced_threshold(block_analysis):
                content_blocks.append(block_analysis)
        
        # Enhanced merging and filtering
        merged_blocks = self.merge_and_filter_blocks_enhanced(content_blocks)
        
        return merged_blocks
    
    def analyze_content_window_enhanced(self, window_lines: List[str], start_idx: int, page_num: int, document_name: str) -> Dict[str, Any]:
        """Enhanced content window analysis"""
        content_text = '\n'.join(window_lines)
        
        analysis = {
            'content': content_text,
            'lines': window_lines,
            'page_number': page_num,
            'document': document_name,
            'start_index': start_idx,
            'word_count': len(content_text.split()),
            'structural_elements': {},
            'content_type': 'general',
            'complexity_score': 0.0,
            'density_score': 0.0,
            'uniqueness_score': 0.0,
            'title': ''
        }
        
        # Enhanced structural analysis
        analysis['structural_elements'] = self.analyze_structural_elements_enhanced(content_text)
        
        # Enhanced content type classification
        analysis['content_type'] = self.classify_content_type_enhanced(window_lines, content_text)
        
        # Enhanced scoring
        analysis['complexity_score'] = self.calculate_structural_complexity_enhanced(analysis)
        analysis['density_score'] = self.calculate_information_density_enhanced(content_text)
        analysis['uniqueness_score'] = self.calculate_structural_uniqueness_enhanced(analysis)
        
        # Enhanced title generation
        analysis['title'] = self.generate_structural_title_enhanced(window_lines, analysis['content_type'])
        
        return analysis
    
    def classify_content_type_enhanced(self, lines: List[str], content_text: str) -> str:
        """Enhanced content type classification"""
        # Check against enhanced document type patterns
        type_scores = {}
        
        for doc_type, pattern_info in self.structural_patterns.items():
            score = 0
            for pattern in pattern_info['indicators']:
                matches = len(re.findall(pattern, content_text, re.MULTILINE | re.IGNORECASE))
                score += matches * pattern_info['weight']
            type_scores[doc_type] = score
        
        if not any(type_scores.values()):
            return 'reference_material'
        
        best_type = max(type_scores.items(), key=lambda x: x[1])[0]
        
        # Map document types to content types
        type_mapping = {
            'travel_guide': 'reference',
            'technical_manual': 'procedural',
            'financial_report': 'informational',
            'reference_material': 'reference'
        }
        
        return type_mapping.get(best_type, 'reference')
    
    def calculate_structural_complexity_enhanced(self, analysis: Dict[str, Any]) -> float:
        """Enhanced complexity calculation"""
        elements = analysis['structural_elements']
        
        # Weight different elements by importance
        element_weights = {
            'bullet_points': 1.0,
            'numbered_lists': 1.2,
            'key_value_pairs': 1.1,
            'measurements': 1.3,
            'proper_nouns': 0.8,
            'contact_info': 1.4,
            'prices': 1.3,
            'time_references': 1.2
        }
        
        weighted_score = 0.0
        total_weight = 0.0
        
        for element, count in elements.items():
            if count > 0:
                weight = element_weights.get(element, 1.0)
                weighted_score += count * weight
                total_weight += weight
        
        if analysis['word_count'] == 0 or total_weight == 0:
            return 0.0
        
        # Normalize by word count and total weight
        complexity = (weighted_score / analysis['word_count']) * (total_weight / len(elements))
        
        return min(complexity * 2, 1.0)  # Scale and cap at 1.0
    
    def calculate_information_density_enhanced(self, content: str) -> float:
        """Enhanced information density calculation"""
        if not content.strip():
            return 0.0
        
        words = content.split()
        word_count = len(words)
        
        if word_count == 0:
            return 0.0
        
        # Enhanced information indicators with better weights
        info_score = 0.0
        
        # High-value information patterns
        info_score += len(re.findall(r'\b\d+(?:\.\d+)?\s*(?:€|$|£|%|km|miles|hours?)\b', content)) * 3.0
        info_score += len(re.findall(r'\b\d{1,2}:\d{2}(?:\s*[ap]m)?\b', content)) * 2.5
        info_score += len(re.findall(r'\b(?:www\.|http|@[\w.-]+)\b', content)) * 2.0
        info_score += len(re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Street|Hotel|Restaurant|Museum))\b', content)) * 1.5
        info_score += len(re.findall(r'^\s*[•\-\*]\s+[A-Z]', content, re.MULTILINE)) * 1.0
        
        return min(info_score / word_count * 10, 2.0)
    
    def calculate_structural_uniqueness_enhanced(self, analysis: Dict[str, Any]) -> float:
        """Enhanced uniqueness calculation"""
        elements = analysis['structural_elements']
        
        # Rare element combinations get higher scores
        uniqueness_score = 0.0
        
        # High-value combinations
        if elements['contact_info'] > 0 and elements['prices'] > 0:
            uniqueness_score += 0.4
        
        if elements['measurements'] > 1 and elements['time_references'] > 0:
            uniqueness_score += 0.3
        
        if elements['numbered_lists'] > 0 and elements['key_value_pairs'] > 2:
            uniqueness_score += 0.3
        
        # Individual rare elements
        rare_elements = ['contact_info', 'prices', 'sub_lists', 'formatted_sections']
        for element in rare_elements:
            if elements.get(element, 0) > 0:
                uniqueness_score += 0.1
        
        return min(uniqueness_score, 1.0)
    
    def generate_structural_title_enhanced(self, lines: List[str], content_type: str) -> str:
        """Enhanced title generation"""
        # Look for the most informative line
        best_title = ""
        best_score = 0
        
        for line in lines[:8]:  # Check more lines
            line_clean = line.strip()
            
            if len(line_clean) < 10 or len(line_clean) > 100:
                continue
            
            score = 0
            
            # Proper nouns indicate specific content
            proper_nouns = len(re.findall(r'\b[A-Z][a-z]{2,}\b', line_clean))
            score += proper_nouns * 2
            
            # Numbers and measurements
            numbers = len(re.findall(r'\b\d+(?:\.\d+)?\b', line_clean))
            score += numbers * 1.5
            
            # Avoid list markers
            if re.match(r'^\s*[•\-\*\+\d+\.\)]\s+', line_clean):
                score -= 2
            
            # Prefer lines with colons (key-value structure)
            if ':' in line_clean and len(line_clean.split(':')) == 2:
                score += 3
            
            # Prefer capitalized words
            caps_words = len(re.findall(r'\b[A-Z][a-z]+\b', line_clean))
            score += caps_words * 0.5
            
            if score > best_score:
                best_score = score
                best_title = line_clean
        
        if best_title:
            # Clean up the title
            best_title = re.sub(r'^\d+[\.\)]\s*', '', best_title)
            best_title = re.sub(r'^[•\-\*\+]\s*', '', best_title)
            
            if len(best_title) > 80:
                best_title = best_title[:77] + "..."
            
            return best_title
        
        # Fallback titles based on content type
        fallback_titles = {
            'procedural': 'Step-by-Step Instructions',
            'informational': 'Information Summary',
            'reference': 'Reference Information',
            'general': 'Content Section'
        }
        
        return fallback_titles.get(content_type, 'Content Section')
    
    def meets_enhanced_threshold(self, analysis: Dict[str, Any]) -> bool:
        """Enhanced threshold checking"""
        # More lenient word count for better coverage
        if analysis['word_count'] < 40:
            return False
        
        # Lower complexity threshold but require some structure
        if analysis['complexity_score'] < 0.15:
            return False
        
        # Require minimum information density
        if analysis['density_score'] < 0.2:
            return False
        
        # Must have at least some structural elements
        total_elements = sum(analysis['structural_elements'].values())
        if total_elements < 1:
            return False
        
        return True
    
    def merge_and_filter_blocks_enhanced(self, content_blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enhanced block merging and filtering"""
        if not content_blocks:
            return []
        
        # Sort by start index
        sorted_blocks = sorted(content_blocks, key=lambda x: x['start_index'])
        merged = []
        
        current_block = sorted_blocks[0]
        
        for next_block in sorted_blocks[1:]:
            # Check for overlap
            current_end = current_block['start_index'] + len(current_block['lines'])
            overlap = max(0, current_end - next_block['start_index'])
            
            if overlap > len(current_block['lines']) * 0.3:  # 30% overlap threshold
                # Keep the block with higher combined score
                current_combined = current_block['complexity_score'] + current_block['density_score']
                next_combined = next_block['complexity_score'] + next_block['density_score']
                
                if next_combined > current_combined:
                    current_block = next_block
            else:
                merged.append(current_block)
                current_block = next_block
        
        merged.append(current_block)
        
        # Enhanced filtering - keep more blocks but ensure quality
        quality_blocks = [block for block in merged if 
                         (block['complexity_score'] + block['density_score']) > 0.4]
        
        # Sort by combined score
        quality_blocks.sort(key=lambda x: (x['complexity_score'] + x['density_score']), reverse=True)
        
        return quality_blocks[:25]  # Return more blocks per document
    
    def calculate_adaptive_relevance(self, block: Dict[str, Any], collection_data: Dict[str, Any]) -> float:
        """Calculate relevance with enhanced weighting"""
        # Enhanced scoring with better balance
        complexity_weight = 0.35
        density_weight = 0.35
        uniqueness_weight = 0.30
        
        final_score = (
            block['complexity_score'] * complexity_weight +
            block['density_score'] * density_weight +
            block['uniqueness_score'] * uniqueness_weight
        )
        
        return min(final_score, 1.0)
    
    def ensure_document_diversity(self, blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ensure diverse representation with enhanced logic"""
        diverse_blocks = []
        doc_counts = {}
        max_per_doc = 4  # Allow more blocks per document
        
        for block in blocks:
            doc_name = block.get('document', '')
            current_count = doc_counts.get(doc_name, 0)
            
            if current_count < max_per_doc:
                diverse_blocks.append(block)
                doc_counts[doc_name] = current_count + 1
            
            if len(diverse_blocks) >= 15:  # Return more total blocks
                break
        
        return diverse_blocks

# Usage example and main function would go here...
def main():
    parser = argparse.ArgumentParser(description='Enhanced Adaptive Document Intelligence System')
    parser.add_argument('--input_dir', required=True, help='Directory containing PDF files')
    parser.add_argument('--persona', default='', help='Optional persona description')
    parser.add_argument('--job', default='', help='Optional job description')
    parser.add_argument('--output', default='enhanced_output.json', help='Output JSON file')
    
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
    print("Using enhanced adaptive structural analysis...")
    
    # Initialize enhanced system
    analyzer = EnhancedAdaptiveDocumentAnalyzer()
    
    # Process documents with enhanced methods
    result = analyzer.process_documents_enhanced(pdf_files, args.persona, args.job)
    
    # Save output
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\nProcessing complete. Output saved to {args.output}")
    print(f"Found {len(result['extracted_sections'])} relevant sections")
    print(f"Discovered {len(result['discovered_personas'])} personas and {len(result['discovered_jobs'])} jobs")
    
    # Print results
    print("\n=== DISCOVERED PERSONAS ===")
    for persona in result['discovered_personas']:
        print(f"- {persona['type']}: {persona['description']} (confidence: {persona['confidence']:.2f})")
    
    print("\n=== DISCOVERED JOBS ===")
    for job in result['discovered_jobs']:
        print(f"- {job['type']}: {job['description']} (confidence: {job['confidence']:.2f})")

if __name__ == "__main__":
    main()
