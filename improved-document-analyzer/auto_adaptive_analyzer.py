#!/usr/bin/env python3

"""
Auto-Adaptive Document Analyzer that automatically detects persona-job combinations
and applies enhanced structural matching without keyword dependencies
"""

import json
import os
import re
from datetime import datetime
from typing import List, Dict, Any, Tuple
import PyPDF2
from collections import Counter, defaultdict
import math

class AutoAdaptiveDocumentAnalyzer:
    def __init__(self):
        # Enhanced structural signatures for automatic detection
        self.document_signatures = {
            'adobe_acrobat_tutorials': {
                'structural_indicators': [
                    r'\b(?:Acrobat|PDF|Adobe)\b',
                    r'\b(?:Select|Click|Choose|Press|Drag|Type)\b.*(?:tool|menu|button|field)\b',
                    r'\b(?:Create|Edit|Export|Share|Fill|Sign|Convert)\b.*(?:PDF|document|form)\b',
                    r'^\s*\d+\.\s+(?:Select|Click|Choose|Open|Navigate)\b'
                ],
                'ui_density_threshold': 0.3,
                'procedural_complexity': 'high',
                'optimal_personas': ['hr_professional', 'business_professional', 'technical_implementer'],
                'optimal_jobs': ['create_manage_forms', 'document_collaboration', 'content_production']
            },
            'travel_guides': {
                'structural_indicators': [
                    r'\b(?:hotel|restaurant|museum|attraction|visit|tour)\b',
                    r'\b(?:€|$|£)\d+(?:\.\d{2})?',
                    r'\b(?:address|phone|hours|open|closed)\b',
                    r'\b(?:Day\s+\d+|Morning|Afternoon|Evening)\b'
                ],
                'location_density_threshold': 0.4,
                'procedural_complexity': 'medium',
                'optimal_personas': ['travel_planner', 'cultural_explorer'],
                'optimal_jobs': ['plan_group_trip', 'discover_activities']
            },
            'business_reports': {
                'structural_indicators': [
                    r'\b(?:revenue|profit|loss|financial|quarterly)\b',
                    r'\b\d+(?:\.\d+)?%',
                    r'\b(?:million|billion|€|$|£)\s*\d+',
                    r'\b(?:Q1|Q2|Q3|Q4|FY\d{4})\b'
                ],
                'data_density_threshold': 0.5,
                'procedural_complexity': 'low',
                'optimal_personas': ['business_analyst', 'financial_analyst'],
                'optimal_jobs': ['analyze_performance', 'generate_reports']
            }
        }
        
        # Enhanced persona-job combinations with structural requirements
        self.persona_job_matrix = {
            'hr_professional': {
                'create_manage_forms': {
                    'required_patterns': [
                        r'\b(?:form|field|fillable|interactive|signature)\b',
                        r'\b(?:create|prepare|design|build).*(?:form|template)\b',
                        r'\b(?:workflow|approval|review|distribute)\b',
                        r'^\s*\d+\.\s+(?:Add|Create|Insert|Configure).*(?:field|form|button)\b'
                    ],
                    'structural_weight': 1.5,
                    'ui_interaction_weight': 1.3,
                    'procedural_depth_requirement': 3
                },
                'document_collaboration': {
                    'required_patterns': [
                        r'\b(?:share|collaborate|review|comment|approve)\b',
                        r'\b(?:signature|sign|authorize|track)\b',
                        r'\b(?:team|group|multiple|recipients)\b',
                        r'^\s*\d+\.\s+(?:Send|Share|Distribute|Request)\b'
                    ],
                    'structural_weight': 1.4,
                    'ui_interaction_weight': 1.2,
                    'procedural_depth_requirement': 2
                }
            },
            'business_professional': {
                'content_production': {
                    'required_patterns': [
                        r'\b(?:create|convert|generate|produce).*(?:document|PDF|content)\b',
                        r'\b(?:edit|modify|format|design)\b',
                        r'\b(?:export|publish|save|output)\b',
                        r'^\s*\d+\.\s+(?:Create|Convert|Generate|Export)\b'
                    ],
                    'structural_weight': 1.3,
                    'ui_interaction_weight': 1.1,
                    'procedural_depth_requirement': 2
                },
                'document_collaboration': {
                    'required_patterns': [
                        r'\b(?:share|collaborate|review|comment)\b',
                        r'\b(?:team|workflow|process|approval)\b',
                        r'\b(?:distribute|collect|manage).*(?:feedback|responses)\b',
                        r'^\s*\d+\.\s+(?:Share|Send|Collaborate|Review)\b'
                    ],
                    'structural_weight': 1.2,
                    'ui_interaction_weight': 1.0,
                    'procedural_depth_requirement': 2
                }
            },
            'technical_implementer': {
                'system_configuration': {
                    'required_patterns': [
                        r'\b(?:configure|setup|install|enable)\b',
                        r'\b(?:settings|preferences|options|properties)\b',
                        r'\b(?:troubleshoot|fix|resolve|debug)\b',
                        r'^\s*\d+\.\s+(?:Configure|Setup|Enable|Install)\b'
                    ],
                    'structural_weight': 1.4,
                    'ui_interaction_weight': 1.3,
                    'procedural_depth_requirement': 3
                }
            }
        }
        
        # Scoring weights for different aspects
        self.scoring_weights = {
            'pattern_match': 0.40,      # How well content matches persona-job patterns
            'structural_quality': 0.25, # Quality of structural organization
            'procedural_depth': 0.20,   # Depth and complexity of procedures
            'ui_interaction': 0.15      # Level of UI interaction described
        }

    def auto_detect_document_type(self, all_content: str) -> str:
        """Automatically detect the document type based on structural patterns"""
        
        type_scores = {}
        word_count = len(all_content.split())
        
        if word_count == 0:
            return 'general'
        
        for doc_type, signature in self.document_signatures.items():
            score = 0.0
            
            # Count pattern matches
            for pattern in signature['structural_indicators']:
                matches = len(re.findall(pattern, all_content, re.IGNORECASE))
                score += matches
            
            # Normalize by content length
            normalized_score = score / word_count * 1000
            type_scores[doc_type] = normalized_score
        
        if not type_scores or max(type_scores.values()) < 1.0:
            return 'general'
        
        return max(type_scores.items(), key=lambda x: x[1])[0]

    def auto_select_optimal_persona_job(self, document_type: str, all_content: str) -> Tuple[str, str]:
        """Automatically select the optimal persona-job combination"""
        
        if document_type not in self.document_signatures:
            return 'business_professional', 'content_production'
        
        signature = self.document_signatures[document_type]
        optimal_personas = signature['optimal_personas']
        optimal_jobs = signature['optimal_jobs']
        
        # Score all persona-job combinations
        best_score = 0.0
        best_persona = optimal_personas[0]
        best_job = optimal_jobs[0]
        
        for persona in optimal_personas:
            if persona in self.persona_job_matrix:
                for job in self.persona_job_matrix[persona]:
                    if job in optimal_jobs:
                        score = self.score_persona_job_fit(all_content, persona, job)
                        if score > best_score:
                            best_score = score
                            best_persona = persona
                            best_job = job
        
        return best_persona, best_job

    def score_persona_job_fit(self, content: str, persona: str, job: str) -> float:
        """Score how well content fits a persona-job combination"""
        
        if persona not in self.persona_job_matrix:
            return 0.0
        
        if job not in self.persona_job_matrix[persona]:
            return 0.0
        
        job_config = self.persona_job_matrix[persona][job]
        
        # Calculate pattern match score
        pattern_score = 0.0
        for pattern in job_config['required_patterns']:
            matches = len(re.findall(pattern, content, re.IGNORECASE | re.MULTILINE))
            pattern_score += matches
        
        # Normalize pattern score
        word_count = len(content.split())
        if word_count > 0:
            pattern_score = (pattern_score / word_count) * 1000
        
        # Calculate structural quality score
        structural_score = self.calculate_structural_quality(content)
        
        # Calculate procedural depth score
        procedural_score = self.calculate_procedural_depth(content)
        
        # Calculate UI interaction score
        ui_score = self.calculate_ui_interaction_level(content)
        
        # Weighted combination
        final_score = (
            pattern_score * self.scoring_weights['pattern_match'] +
            structural_score * self.scoring_weights['structural_quality'] +
            procedural_score * self.scoring_weights['procedural_depth'] +
            ui_score * self.scoring_weights['ui_interaction']
        )
        
        return final_score

    def calculate_structural_quality(self, content: str) -> float:
        """Calculate the structural quality of content"""
        
        # Count structural elements
        numbered_lists = len(re.findall(r'^\s*\d+\.\s+', content, re.MULTILINE))
        bullet_points = len(re.findall(r'^\s*[•\-\*]\s+', content, re.MULTILINE))
        sub_lists = len(re.findall(r'^\s*[a-z]\)\s+', content, re.MULTILINE))
        headers = len(re.findall(r'^[A-Z][A-Z\s]{5,}$', content, re.MULTILINE))
        
        # Calculate quality score
        quality_score = (
            numbered_lists * 1.2 +
            bullet_points * 1.0 +
            sub_lists * 1.1 +
            headers * 0.8
        )
        
        # Normalize by content length
        word_count = len(content.split())
        if word_count > 0:
            quality_score = (quality_score / word_count) * 100
        
        return min(quality_score, 1.0)

    def calculate_procedural_depth(self, content: str) -> float:
        """Calculate the procedural depth and complexity"""
        
        # Look for sequential indicators
        sequential_words = len(re.findall(r'\b(?:first|second|third|next|then|finally|after|before)\b', content, re.IGNORECASE))
        
        # Look for conditional logic
        conditional_words = len(re.findall(r'\b(?:if|when|unless|should|depending|based on)\b', content, re.IGNORECASE))
        
        # Look for hierarchical structure
        indented_lines = len(re.findall(r'^\s{4,}[^\s]', content, re.MULTILINE))
        
        # Calculate depth score
        depth_score = (
            sequential_words * 0.5 +
            conditional_words * 0.7 +
            indented_lines * 0.3
        )
        
        # Normalize by content length
        word_count = len(content.split())
        if word_count > 0:
            depth_score = (depth_score / word_count) * 100
        
        return min(depth_score, 1.0)

    def calculate_ui_interaction_level(self, content: str) -> float:
        """Calculate the level of UI interaction described"""
        
        # UI action verbs
        ui_actions = len(re.findall(r'\b(?:click|select|choose|press|drag|drop|type|enter|hover|scroll)\b', content, re.IGNORECASE))
        
        # UI elements
        ui_elements = len(re.findall(r'\b(?:button|menu|toolbar|panel|dialog|window|field|checkbox|dropdown|tab)\b', content, re.IGNORECASE))
        
        # Specific UI references
        specific_ui = len(re.findall(r'\b(?:All tools|File menu|Edit menu|View menu|Properties panel)\b', content, re.IGNORECASE))
        
        # Calculate UI score
        ui_score = (
            ui_actions * 1.0 +
            ui_elements * 0.8 +
            specific_ui * 1.2
        )
        
        # Normalize by content length
        word_count = len(content.split())
        if word_count > 0:
            ui_score = (ui_score / word_count) * 100
        
        return min(ui_score, 1.0)

    def extract_enhanced_sections(self, pdf_paths: List[str], persona: str, job: str) -> List[Dict[str, Any]]:
        """Extract sections with enhanced persona-job matching"""
        
        all_sections = []
        
        for pdf_path in pdf_paths:
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    document_name = os.path.basename(pdf_path)
                    
                    for page_num, page in enumerate(pdf_reader.pages, 1):
                        page_text = page.extract_text()
                        page_sections = self.extract_sections_from_page_enhanced(
                            page_text, page_num, document_name, persona, job
                        )
                        all_sections.extend(page_sections)
            
            except Exception as e:
                print(f"Error processing {pdf_path}: {e}")
                continue
        
        # Sort by relevance score
        all_sections.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        # Ensure document diversity
        diverse_sections = self.ensure_document_diversity_enhanced(all_sections)
        
        return diverse_sections

    def extract_sections_from_page_enhanced(self, page_text: str, page_num: int, document_name: str, persona: str, job: str) -> List[Dict[str, Any]]:
        """Extract sections from a page with enhanced persona-job matching"""
        
        lines = [line.strip() for line in page_text.split('\n') if line.strip()]
        sections = []
        
        if len(lines) < 5:
            return sections
        
        # Use sliding window approach
        window_size = 12
        step_size = 6
        
        for i in range(0, len(lines) - window_size + 1, step_size):
            window_lines = lines[i:i + window_size]
            content_text = '\n'.join(window_lines)
            
            # Calculate enhanced relevance score
            relevance_score = self.calculate_enhanced_relevance_score(content_text, persona, job)
            
            if relevance_score > 0.3:  # Threshold for inclusion
                section = {
                    'content': content_text,
                    'lines': window_lines,
                    'page_number': page_num,
                    'document': document_name,
                    'word_count': len(content_text.split()),
                    'relevance_score': relevance_score,
                    'title': self.generate_enhanced_title(window_lines, persona, job)
                }
                sections.append(section)
        
        # Merge overlapping sections
        merged_sections = self.merge_overlapping_sections_enhanced(sections)
        
        return merged_sections

    def calculate_enhanced_relevance_score(self, content: str, persona: str, job: str) -> float:
        """Calculate enhanced relevance score for persona-job combination"""
        
        # Get the persona-job configuration
        if persona not in self.persona_job_matrix or job not in self.persona_job_matrix[persona]:
            return 0.0
        
        job_config = self.persona_job_matrix[persona][job]
        
        # Calculate pattern match score
        pattern_score = 0.0
        for pattern in job_config['required_patterns']:
            matches = len(re.findall(pattern, content, re.IGNORECASE | re.MULTILINE))
            pattern_score += matches
        
        # Apply structural weight
        pattern_score *= job_config['structural_weight']
        
        # Calculate other scores
        structural_score = self.calculate_structural_quality(content)
        procedural_score = self.calculate_procedural_depth(content)
        ui_score = self.calculate_ui_interaction_level(content)
        
        # Apply UI interaction weight
        ui_score *= job_config['ui_interaction_weight']
        
        # Weighted combination
        final_score = (
            pattern_score * self.scoring_weights['pattern_match'] +
            structural_score * self.scoring_weights['structural_quality'] +
            procedural_score * self.scoring_weights['procedural_depth'] +
            ui_score * self.scoring_weights['ui_interaction']
        )
        
        return min(final_score, 1.0)

    def generate_enhanced_title(self, lines: List[str], persona: str, job: str) -> str:
        """Generate enhanced title based on persona-job context"""
        
        # Look for the most relevant line based on persona-job
        best_title = ""
        best_score = 0
        
        for line in lines[:6]:
            line_clean = line.strip()
            
            if len(line_clean) < 8 or len(line_clean) > 120:
                continue
            
            score = 0
            
            # Score based on persona-job relevance
            if persona == 'hr_professional' and job == 'create_manage_forms':
                if re.search(r'\b(?:form|field|fillable|signature|workflow)\b', line_clean, re.IGNORECASE):
                    score += 3
                if re.search(r'\b(?:create|prepare|design|manage)\b', line_clean, re.IGNORECASE):
                    score += 2
            
            elif persona == 'business_professional' and job == 'document_collaboration':
                if re.search(r'\b(?:share|collaborate|review|comment|approve)\b', line_clean, re.IGNORECASE):
                    score += 3
                if re.search(r'\b(?:team|group|workflow|process)\b', line_clean, re.IGNORECASE):
                    score += 2
            
            elif job == 'content_production':
                if re.search(r'\b(?:create|convert|generate|export|produce)\b', line_clean, re.IGNORECASE):
                    score += 3
                if re.search(r'\b(?:document|PDF|file|content)\b', line_clean, re.IGNORECASE):
                    score += 2
            
            # General scoring
            if re.search(r'\b(?:Adobe|Acrobat|PDF)\b', line_clean, re.IGNORECASE):
                score += 1
            
            # Prefer lines that look like headers or instructions
            if re.match(r'^[A-Z]', line_clean) and not re.match(r'^\d+\.', line_clean):
                score += 1
            
            # Avoid generic selections
            if line_clean.lower().startswith(('select', 'click', 'choose')) and len(line_clean) < 30:
                score -= 2
            
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
        
        # Fallback based on persona-job
        fallback_titles = {
            ('hr_professional', 'create_manage_forms'): 'Form Creation and Management',
            ('business_professional', 'document_collaboration'): 'Document Collaboration Process',
            ('business_professional', 'content_production'): 'Content Creation Process',
            ('technical_implementer', 'system_configuration'): 'System Configuration Steps'
        }
        
        return fallback_titles.get((persona, job), 'Document Process')

    def merge_overlapping_sections_enhanced(self, sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Merge overlapping sections with enhanced logic"""
        
        if not sections:
            return []
        
        # Sort by relevance score
        sorted_sections = sorted(sections, key=lambda x: x['relevance_score'], reverse=True)
        merged = []
        
        for section in sorted_sections:
            # Check if this section overlaps significantly with any existing merged section
            is_duplicate = False
            
            for existing in merged:
                # Simple overlap check based on content similarity
                overlap_ratio = self.calculate_content_overlap(section['content'], existing['content'])
                if overlap_ratio > 0.6:  # 60% overlap threshold
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                merged.append(section)
            
            # Limit sections per document
            if len(merged) >= 20:
                break
        
        return merged

    def calculate_content_overlap(self, content1: str, content2: str) -> float:
        """Calculate content overlap ratio between two text blocks"""
        
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0

    def ensure_document_diversity_enhanced(self, sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ensure diverse representation across documents"""
        
        diverse_sections = []
        doc_counts = {}
        max_per_doc = 3  # Limit per document
        
        for section in sections:
            doc_name = section.get('document', '')
            current_count = doc_counts.get(doc_name, 0)
            
            if current_count < max_per_doc:
                diverse_sections.append(section)
                doc_counts[doc_name] = current_count + 1
            
            if len(diverse_sections) >= 10:  # Total limit
                break
        
        return diverse_sections

    def process_documents_auto_adaptive(self, pdf_paths: List[str], input_persona: str = "", input_job: str = "") -> Dict[str, Any]:
        """Main processing function with auto-adaptive capabilities"""
        
        start_time = datetime.now()
        
        print("🤖 Starting Auto-Adaptive Document Analysis")
        print("=" * 60)
        
        # Read all content for analysis
        all_content = ""
        for pdf_path in pdf_paths:
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        all_content += page.extract_text() + "\n"
            except Exception as e:
                print(f"Error reading {pdf_path}: {e}")
                continue
        
        print(f"📚 Analyzed {len(all_content.split())} words across {len(pdf_paths)} documents")
        
        # Auto-detect document type
        document_type = self.auto_detect_document_type(all_content)
        print(f"🔍 Detected document type: {document_type}")
        
        # Auto-select optimal persona-job combination
        if not input_persona or not input_job:
            optimal_persona, optimal_job = self.auto_select_optimal_persona_job(document_type, all_content)
            effective_persona = input_persona if input_persona else optimal_persona
            effective_job = input_job if input_job else optimal_job
            
            print(f"🎯 Auto-selected persona: {effective_persona}")
            print(f"🎯 Auto-selected job: {effective_job}")
        else:
            effective_persona = input_persona
            effective_job = input_job
            print(f"👤 Using provided persona: {effective_persona}")
            print(f"💼 Using provided job: {effective_job}")
        
        # Extract sections with enhanced matching
        print(f"\n🚀 Extracting sections with enhanced {effective_persona} + {effective_job} matching...")
        enhanced_sections = self.extract_enhanced_sections(pdf_paths, effective_persona, effective_job)
        
        print(f"✅ Extracted {len(enhanced_sections)} relevant sections")
        
        # Prepare output
        result = {
            "metadata": {
                "input_documents": [os.path.basename(path) for path in pdf_paths],
                "original_persona": input_persona,
                "original_job": input_job,
                "effective_persona": effective_persona,
                "effective_job": effective_job,
                "detected_document_type": document_type,
                "processing_timestamp": start_time.isoformat(),
                "analysis_method": "auto_adaptive_structural_analysis"
            },
            "extracted_sections": [],
            "subsection_analysis": []
        }
        
        # Add extracted sections
        for rank, section in enumerate(enhanced_sections[:5], 1):
            result["extracted_sections"].append({
                "document": section["document"],
                "section_title": section["title"],
                "importance_rank": rank,
                "page_number": section["page_number"],
                "relevance_score": round(section["relevance_score"], 3),
                "word_count": section["word_count"]
            })
        
        # Add subsection analysis
        for section in enhanced_sections[:3]:
            refined_text = section['content'][:500] + "..." if len(section['content']) > 500 else section['content']
            result["subsection_analysis"].append({
                "document": section["document"],
                "refined_text": refined_text,
                "page_number": section["page_number"],
                "parent_section": section["title"]
            })
        
        return result

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Auto-Adaptive Document Intelligence System')
    parser.add_argument('--input_dir', required=True, help='Directory containing PDF files')
    parser.add_argument('--persona', default='', help='Optional persona (auto-detected if not provided)')
    parser.add_argument('--job', default='', help='Optional job (auto-detected if not provided)')
    parser.add_argument('--output', default='auto_adaptive_results.json', help='Output JSON file')
    
    args = parser.parse_args()
    
    # Find PDF files
    pdf_files = []
    for file in os.listdir(args.input_dir):
        if file.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(args.input_dir, file))
    
    if not pdf_files:
        print("❌ No PDF files found in input directory")
        return
    
    print(f"📁 Found {len(pdf_files)} PDF files")
    
    # Initialize auto-adaptive analyzer
    analyzer = AutoAdaptiveDocumentAnalyzer()
    
    # Process documents
    result = analyzer.process_documents_auto_adaptive(pdf_files, args.persona, args.job)
    
    # Save results
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Analysis complete! Results saved to {args.output}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 RESULTS SUMMARY")
    print("=" * 60)
    print(f"Document Type: {result['metadata']['detected_document_type']}")
    print(f"Effective Persona: {result['metadata']['effective_persona']}")
    print(f"Effective Job: {result['metadata']['effective_job']}")
    print(f"Sections Found: {len(result['extracted_sections'])}")
    
    print(f"\n📄 TOP SECTIONS:")
    for section in result['extracted_sections']:
        print(f"{section['importance_rank']}. {section['section_title']}")
        print(f"   Document: {section['document']} | Page: {section['page_number']} | Score: {section['relevance_score']}")

if __name__ == "__main__":
    main()
