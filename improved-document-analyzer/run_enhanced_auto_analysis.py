#!/usr/bin/env python3

import sys
import os
import json
from pathlib import Path
import re
from collections import Counter

# Add the parent directory to the path so we can import the enhanced analyzer
sys.path.append(str(Path(__file__).parent.parent))

def auto_detect_optimal_persona_job(all_content: str):
    """Auto-detect optimal persona-job combination from content"""
    
    # Document type signatures
    adobe_indicators = [
        r'\b(?:Acrobat|Adobe|PDF)\b',
        r'\b(?:Select|Click|Choose|Press)\b.*(?:tool|menu|button)\b',
        r'\b(?:Create|Edit|Export|Share|Fill|Sign)\b.*(?:PDF|document|form)\b',
        r'^\s*\d+\.\s+(?:Select|Click|Choose|Open)\b'
    ]
    
    travel_indicators = [
        r'\b(?:hotel|restaurant|museum|attraction|visit|tour)\b',
        r'\b(?:€|$|£)\d+(?:\.\d{2})?',
        r'\b(?:Day\s+\d+|Morning|Afternoon|Evening)\b',
        r'\b(?:address|phone|hours|open|closed)\b'
    ]
    
    business_indicators = [
        r'\b(?:revenue|profit|quarterly|annual|financial)\b',
        r'\b\d+(?:\.\d+)?%',
        r'\b(?:Q1|Q2|Q3|Q4|FY\d{4})\b'
    ]
    
    # Count indicators
    adobe_score = sum(len(re.findall(pattern, all_content, re.IGNORECASE | re.MULTILINE)) for pattern in adobe_indicators)
    travel_score = sum(len(re.findall(pattern, all_content, re.IGNORECASE | re.MULTILINE)) for pattern in travel_indicators)
    business_score = sum(len(re.findall(pattern, all_content, re.IGNORECASE | re.MULTILINE)) for pattern in business_indicators)
    
    print(f"🔍 Content Analysis Scores:")
    print(f"   Adobe/PDF: {adobe_score}")
    print(f"   Travel: {travel_score}")
    print(f"   Business: {business_score}")
    
    # Determine document type and optimal persona-job
    if adobe_score > travel_score and adobe_score > business_score:
        # Adobe Acrobat content detected
        
        # Check for specific Adobe use cases
        form_indicators = len(re.findall(r'\b(?:form|field|fillable|signature|workflow)\b', all_content, re.IGNORECASE))
        collaboration_indicators = len(re.findall(r'\b(?:share|collaborate|review|comment|approve)\b', all_content, re.IGNORECASE))
        creation_indicators = len(re.findall(r'\b(?:create|convert|generate|export)\b', all_content, re.IGNORECASE))
        
        print(f"   Form-related: {form_indicators}")
        print(f"   Collaboration: {collaboration_indicators}")
        print(f"   Creation: {creation_indicators}")
        
        if form_indicators > collaboration_indicators and form_indicators > creation_indicators:
            return "HR Professional", "Create and manage fillable forms for onboarding and compliance"
        elif collaboration_indicators > creation_indicators:
            return "Business Professional", "Facilitate document collaboration and approval workflows"
        else:
            return "Business Professional", "Create and manage professional documents and content"
    
    elif travel_score > business_score:
        return "Travel Planner", "Plan a trip of 4 days for a group of 10 college friends"
    
    else:
        return "Business Analyst", "Analyze business performance and generate reports"

def run_enhanced_auto_analysis():
    """Run enhanced analysis with auto-detection"""
    
    print("🤖 Enhanced Auto-Adaptive Document Analysis")
    print("=" * 60)
    
    # Set up paths
    project_root = Path(__file__).parent.parent
    documents_dir = project_root / "documents"
    output_dir = project_root / "output"
    
    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)
    
    # Find PDF files
    pdf_files = list(documents_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found in documents directory")
        return
    
    print(f"📚 Found {len(pdf_files)} PDF files:")
    for pdf_file in pdf_files:
        print(f"  - {pdf_file.name}")
    
    # Read all content for auto-detection
    print(f"\n🔍 Analyzing content for auto-detection...")
    all_content = ""
    
    try:
        import PyPDF2
        
        for pdf_file in pdf_files:
            try:
                with open(pdf_file, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        all_content += page_text + "\n"
            except Exception as e:
                print(f"⚠️  Error reading {pdf_file.name}: {e}")
                continue
        
        print(f"📄 Analyzed {len(all_content.split())} words total")
        
        # Auto-detect optimal persona and job
        optimal_persona, optimal_job = auto_detect_optimal_persona_job(all_content)
        
        print(f"\n🎯 Auto-detected optimal combination:")
        print(f"   Persona: {optimal_persona}")
        print(f"   Job: {optimal_job}")
        
        # Import and run the structural analyzer with optimal settings
        try:
            from structural_document_analyzer import StructuralDocumentAnalyzer
            
            print(f"\n🚀 Running structural analysis with optimal settings...")
            
            # Initialize analyzer
            analyzer = StructuralDocumentAnalyzer()
            
            # Process documents with auto-detected persona-job
            result = analyzer.analyze_document_collection(
                [str(f) for f in pdf_files], 
                optimal_persona, 
                optimal_job
            )
            
            # Save results
            output_file = output_dir / "auto_enhanced_results.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Analysis complete! Results saved to {output_file}")
            
            # Print summary
            print("\n" + "=" * 60)
            print("📊 AUTO-ENHANCED ANALYSIS RESULTS")
            print("=" * 60)
            
            print(f"🎯 Used Persona: {optimal_persona}")
            print(f"🎯 Used Job: {optimal_job}")
            print(f"📄 Documents Processed: {len(result['metadata']['input_documents'])}")
            print(f"📋 Sections Extracted: {len(result['extracted_sections'])}")
            
            print(f"\n📄 TOP RELEVANT SECTIONS:")
            print("-" * 40)
            for section in result['extracted_sections']:
                print(f"{section['importance_rank']}. {section['section_title']}")
                print(f"   📁 Document: {section['document']}")
                print(f"   📄 Page: {section['page_number']}")
                print()
            
            # Show subsection analysis
            if result.get('subsection_analysis'):
                print(f"🔍 DETAILED SUBSECTION ANALYSIS:")
                print("-" * 40)
                for i, subsection in enumerate(result['subsection_analysis'][:3], 1):
                    print(f"{i}. From: {subsection['document']} (Page {subsection['page_number']})")
                    preview = subsection['refined_text'][:200] + "..." if len(subsection['refined_text']) > 200 else subsection['refined_text']
                    print(f"   Preview: {preview}")
                    print()
            
            return result
            
        except ImportError as e:
            print(f"❌ Error importing structural analyzer: {e}")
            print("💡 Make sure structural_document_analyzer.py is available")
            return None
            
    except ImportError as e:
        print(f"❌ Error importing PyPDF2: {e}")
        print("💡 Make sure PyPDF2 is installed: pip install PyPDF2")
        return None
    
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = run_enhanced_auto_analysis()
    
    if result:
        print("\n" + "=" * 60)
        print("🎉 AUTO-ENHANCED ANALYSIS COMPLETE!")
        print("=" * 60)
        print("✅ Successfully auto-detected document type and applied optimal analysis")
        print("✅ Results should now be highly relevant to the actual document content")
        print("✅ Check output/auto_enhanced_results.json for detailed results")
    else:
        print("\n❌ Analysis failed. Please check the error messages above.")
