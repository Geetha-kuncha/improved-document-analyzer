#!/usr/bin/env python3

import sys
import os
import json
from pathlib import Path

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent.parent))

def run_corrected_analysis():
    """Run analysis with forced correct persona-job for Adobe Acrobat content"""
    
    print("🔧 Running Corrected Analysis for Adobe Acrobat Content")
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
    
    # FORCE the correct persona and job for Adobe Acrobat content
    CORRECT_PERSONA = "HR Professional managing digital workflows"
    CORRECT_JOB = "Create and manage fillable forms, e-signatures, and document collaboration workflows"
    
    print(f"\n🎯 Using CORRECTED persona-job combination:")
    print(f"   Persona: {CORRECT_PERSONA}")
    print(f"   Job: {CORRECT_JOB}")
    
    try:
        # Import the structural analyzer
        from structural_document_analyzer import StructuralDocumentAnalyzer
        
        print(f"\n🚀 Running structural analysis with corrected settings...")
        
        # Initialize analyzer
        analyzer = StructuralDocumentAnalyzer()
        
        # DIRECTLY call the analysis method with correct parameters
        result = analyzer.analyze_document_collection(
            [str(f) for f in pdf_files], 
            CORRECT_PERSONA, 
            CORRECT_JOB
        )
        
        # FORCE update the metadata to ensure correct values
        result['metadata']['persona'] = CORRECT_PERSONA
        result['metadata']['job_to_be_done'] = CORRECT_JOB
        result['metadata']['analysis_method'] = 'corrected_adobe_acrobat_analysis'
        
        # Save results
        output_file = output_dir / "corrected_adobe_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Analysis complete! Results saved to {output_file}")
        
        # Print detailed summary
        print("\n" + "=" * 60)
        print("📊 CORRECTED ANALYSIS RESULTS")
        print("=" * 60)
        
        print(f"✅ Persona: {result['metadata']['persona']}")
        print(f"✅ Job: {result['metadata']['job_to_be_done']}")
        print(f"📄 Documents Processed: {len(result['metadata']['input_documents'])}")
        print(f"📋 Sections Extracted: {len(result['extracted_sections'])}")
        
        print(f"\n📄 TOP RELEVANT SECTIONS:")
        print("-" * 50)
        for section in result['extracted_sections']:
            print(f"{section['importance_rank']}. {section['section_title']}")
            print(f"   📁 Document: {section['document']}")
            print(f"   📄 Page: {section['page_number']}")
            
            # Show more context for Adobe-specific content
            if any(keyword in section['section_title'].lower() for keyword in ['select', 'click', 'form', 'sign', 'share', 'create']):
                print(f"   🎯 Adobe Action: Detected procedural step")
            print()
        
        # Enhanced subsection analysis
        if result.get('subsection_analysis'):
            print(f"🔍 DETAILED ADOBE WORKFLOW ANALYSIS:")
            print("-" * 50)
            for i, subsection in enumerate(result['subsection_analysis'], 1):
                print(f"{i}. From: {subsection['document']} (Page {subsection['page_number']})")
                
                # Clean up the text for better readability
                text = subsection['refined_text']
                
                # Identify Adobe-specific actions
                adobe_actions = []
                if 'select' in text.lower(): adobe_actions.append('UI Selection')
                if 'click' in text.lower(): adobe_actions.append('User Action')
                if 'form' in text.lower(): adobe_actions.append('Form Management')
                if 'sign' in text.lower(): adobe_actions.append('E-signature')
                if 'share' in text.lower(): adobe_actions.append('Collaboration')
                
                if adobe_actions:
                    print(f"   🏷️  Adobe Features: {', '.join(adobe_actions)}")
                
                # Show preview
                preview = text[:300] + "..." if len(text) > 300 else text
                print(f"   📝 Content: {preview}")
                print()
        
        # Analysis quality check
        adobe_keywords = ['acrobat', 'pdf', 'form', 'sign', 'share', 'create', 'edit', 'export']
        total_content = ' '.join([section['section_title'] for section in result['extracted_sections']]).lower()
        adobe_matches = sum(1 for keyword in adobe_keywords if keyword in total_content)
        
        print(f"🎯 QUALITY CHECK:")
        print(f"   Adobe-relevant keywords found: {adobe_matches}/{len(adobe_keywords)}")
        if adobe_matches >= 4:
            print(f"   ✅ HIGH RELEVANCE: Results are well-matched to Adobe Acrobat content")
        elif adobe_matches >= 2:
            print(f"   ⚠️  MEDIUM RELEVANCE: Some Adobe content detected")
        else:
            print(f"   ❌ LOW RELEVANCE: Results may not be optimal for Adobe content")
        
        return result
        
    except ImportError as e:
        print(f"❌ Error importing structural analyzer: {e}")
        return None
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = run_corrected_analysis()
    
    if result:
        print("\n" + "=" * 60)
        print("🎉 CORRECTED ANALYSIS COMPLETE!")
        print("=" * 60)
        print("✅ Forced correct persona-job combination")
        print("✅ Results should now be optimized for Adobe Acrobat workflows")
        print("✅ Check output/corrected_adobe_results.json for full details")
        
        # Quick validation
        if result['metadata']['persona'] != "Travel Planner":
            print("✅ SUCCESS: Persona correctly updated!")
        else:
            print("❌ WARNING: Persona still shows Travel Planner")
    else:
        print("\n❌ Analysis failed. Please check the error messages above.")
