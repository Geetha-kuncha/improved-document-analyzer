#!/usr/bin/env python3

import sys
import os
import json
from pathlib import Path
import PyPDF2
from collections import Counter, defaultdict
import re

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent.parent))

def diagnose_documents():
    """Diagnose the document collection to understand why personas/jobs might be empty"""
    
    print("🔍 DIAGNOSTIC ANALYSIS")
    print("=" * 60)
    
    project_root = Path(__file__).parent.parent
    documents_dir = project_root / "documents"
    
    pdf_files = list(documents_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    print(f"📚 Analyzing {len(pdf_files)} documents...")
    
    all_text = ""
    all_structural_elements = defaultdict(int)
    document_analysis = {}
    
    for pdf_file in pdf_files:
        print(f"\n📄 Analyzing: {pdf_file.name}")
        
        try:
            with open(pdf_file, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                doc_text = ""
                
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    doc_text += page_text
                    all_text += page_text
                
                # Analyze this document
                doc_analysis = analyze_single_document(doc_text, pdf_file.name)
                document_analysis[pdf_file.name] = doc_analysis
                
                # Aggregate structural elements
                for element, count in doc_analysis['structural_elements'].items():
                    all_structural_elements[element] += count
                
                print(f"  📊 Word count: {doc_analysis['word_count']}")
                print(f"  🏗️  Top structural elements:")
                top_elements = sorted(doc_analysis['structural_elements'].items(), 
                                    key=lambda x: x[1], reverse=True)[:5]
                for element, count in top_elements:
                    if count > 0:
                        print(f"    - {element}: {count}")
        
        except Exception as e:
            print(f"  ❌ Error reading {pdf_file.name}: {e}")
    
    # Overall analysis
    print(f"\n" + "=" * 60)
    print("📊 COLLECTION ANALYSIS")
    print("=" * 60)
    
    total_words = len(all_text.split())
    print(f"Total words across all documents: {total_words:,}")
    
    print(f"\n🏗️  Structural Elements Across Collection:")
    sorted_elements = sorted(all_structural_elements.items(), key=lambda x: x[1], reverse=True)
    for element, count in sorted_elements:
        if count > 0:
            density = count / total_words * 1000 if total_words > 0 else 0
            print(f"  {element}: {count} (density: {density:.2f} per 1000 words)")
    
    # Content analysis
    print(f"\n📝 CONTENT ANALYSIS:")
    content_lower = all_text.lower()
    
    # Travel-related keywords
    travel_keywords = ['travel', 'trip', 'visit', 'destination', 'hotel', 'restaurant', 'attraction', 'guide', 'tourism', 'vacation']
    travel_count = sum(content_lower.count(keyword) for keyword in travel_keywords)
    print(f"  Travel-related terms: {travel_count}")
    
    # Business-related keywords
    business_keywords = ['analysis', 'report', 'data', 'metrics', 'performance', 'revenue', 'profit', 'business']
    business_count = sum(content_lower.count(keyword) for keyword in business_keywords)
    print(f"  Business-related terms: {business_count}")
    
    # Cultural keywords
    cultural_keywords = ['culture', 'history', 'museum', 'art', 'heritage', 'tradition', 'historical', 'cultural']
    cultural_count = sum(content_lower.count(keyword) for keyword in cultural_keywords)
    print(f"  Cultural-related terms: {cultural_count}")
    
    # Technical keywords
    technical_keywords = ['installation', 'setup', 'configuration', 'system', 'software', 'technical', 'manual']
    technical_count = sum(content_lower.count(keyword) for keyword in technical_keywords)
    print(f"  Technical-related terms: {technical_count}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    
    if travel_count > 50:
        print("  ✅ Strong travel content detected - should discover travel_planner persona")
    else:
        print("  ⚠️  Low travel content - may not detect travel_planner persona")
    
    if cultural_count > 30:
        print("  ✅ Strong cultural content detected - should discover cultural_explorer persona")
    else:
        print("  ⚠️  Low cultural content - may not detect cultural_explorer persona")
    
    if all_structural_elements['bullet_points'] > 50:
        print("  ✅ Good structural organization - should help with job detection")
    else:
        print("  ⚠️  Low structural organization - may affect job detection")
    
    if all_structural_elements['proper_nouns'] > 100:
        print("  ✅ Rich proper noun content - good for persona detection")
    else:
        print("  ⚠️  Low proper noun density - may affect persona detection")
    
    # Save diagnostic results
    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True)
    
    diagnostic_results = {
        'total_documents': len(pdf_files),
        'total_words': total_words,
        'structural_elements': dict(all_structural_elements),
        'content_keywords': {
            'travel': travel_count,
            'business': business_count,
            'cultural': cultural_count,
            'technical': technical_count
        },
        'document_analysis': document_analysis
    }
    
    with open(output_dir / "diagnostic_results.json", 'w', encoding='utf-8') as f:
        json.dump(diagnostic_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Diagnostic results saved to output/diagnostic_results.json")
    
    return diagnostic_results

def analyze_single_document(text: str, filename: str) -> dict:
    """Analyze a single document for diagnostic purposes"""
    
    analysis = {
        'filename': filename,
        'word_count': len(text.split()),
        'structural_elements': {},
        'content_indicators': {}
    }
    
    # Structural elements analysis
    structural_elements = {
        'bullet_points': len(re.findall(r'^\s*[•\-\*\+]\s+\w', text, re.MULTILINE)),
        'numbered_lists': len(re.findall(r'^\s*\d+[\.\)]\s+\w', text, re.MULTILINE)),
        'key_value_pairs': len(re.findall(r'^[^:\n]{3,40}:\s*[^:\n]{10,}', text, re.MULTILINE)),
        'measurements': len(re.findall(r'\b\d+(?:\.\d+)?\s*(?:km|miles|hours?|days?|minutes?|euros?|€|$|£|%)\b', text, re.IGNORECASE)),
        'proper_nouns': len(re.findall(r'\b[A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})*\b', text)),
        'contact_info': len(re.findall(r'\b(?:www\.|http|@[\w.-]+|\+?\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4})\b', text)),
        'prices': len(re.findall(r'\b(?:€|$|£)\s*\d+(?:\.\d{2})?|\b\d+(?:\.\d{2})?\s*(?:euros?|dollars?|pounds?)\b', text, re.IGNORECASE)),
        'time_references': len(re.findall(r'\b(?:\d{1,2}:\d{2}|\d{1,2}[ap]m|morning|afternoon|evening|night|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b', text, re.IGNORECASE)),
        'locations': len(re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Street|St|Avenue|Ave|Road|Rd|Square|Place|Center|Centre|Museum|Hotel|Restaurant))\b', text))
    }
    
    analysis['structural_elements'] = structural_elements
    
    return analysis

if __name__ == "__main__":
    diagnose_documents()
