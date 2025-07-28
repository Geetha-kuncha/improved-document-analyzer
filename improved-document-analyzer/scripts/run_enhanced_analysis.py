#!/usr/bin/env python3

import sys
import os
import json
from pathlib import Path

# Add the parent directory to the path so we can import the enhanced analyzer
sys.path.append(str(Path(__file__).parent.parent))

# Import the enhanced analyzer
from enhanced_adaptive_analyzer import EnhancedAdaptiveDocumentAnalyzer

def run_enhanced_analysis():
    """Run the enhanced analysis on the South of France documents"""
    
    print("🔍 Running Enhanced Adaptive Document Analysis")
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
    
    print("\n🚀 Starting enhanced analysis...")
    
    # Initialize enhanced analyzer
    analyzer = EnhancedAdaptiveDocumentAnalyzer()
    
    # Process documents
    try:
        result = analyzer.process_documents_enhanced([str(f) for f in pdf_files])
        
        # Save results
        output_file = output_dir / "enhanced_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Analysis complete! Results saved to {output_file}")
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 ANALYSIS SUMMARY")
        print("=" * 60)
        
        # Collection Profile
        profile = result['metadata']['collection_profile']
        print(f"📁 Collection Focus: {profile['collection_focus']}")
        print(f"📄 Dominant Document Type: {profile['dominant_document_type']}")
        print(f"🎯 Content Diversity: {profile['content_diversity']:.2f}")
        print(f"📈 Information Richness: {profile['information_richness']:.2f}")
        print(f"🔧 Structural Consistency: {profile['structural_consistency']:.2f}")
        
        # Discovered Personas
        print(f"\n👥 DISCOVERED PERSONAS ({len(result['discovered_personas'])})")
        print("-" * 40)
        if result['discovered_personas']:
            for i, persona in enumerate(result['discovered_personas'], 1):
                print(f"{i}. {persona['type'].replace('_', ' ').title()}")
                print(f"   Description: {persona['description']}")
                print(f"   Confidence: {persona['confidence']:.2f} ({persona['confidence']*100:.1f}%)")
                print()
        else:
            print("❌ No personas discovered - this indicates an issue with the analysis")
        
        # Discovered Jobs
        print(f"🎯 DISCOVERED JOBS ({len(result['discovered_jobs'])})")
        print("-" * 40)
        if result['discovered_jobs']:
            for i, job in enumerate(result['discovered_jobs'], 1):
                print(f"{i}. {job['type'].replace('_', ' ').title()}")
                print(f"   Description: {job['description']}")
                print(f"   Confidence: {job['confidence']:.2f} ({job['confidence']*100:.1f}%)")
                print()
        else:
            print("❌ No jobs discovered - this indicates an issue with the analysis")
        
        # Structural Patterns
        patterns = result['structural_patterns']
        print(f"🏗️  STRUCTURAL PATTERNS")
        print("-" * 40)
        print(f"Common Structures: {', '.join(patterns['common_structures'][:5])}")
        print(f"Rare Structures: {', '.join(patterns['rare_structures'][:3])}")
        
        # Top Sections
        print(f"\n📄 TOP RELEVANT SECTIONS ({len(result['extracted_sections'])})")
        print("-" * 40)
        for i, section in enumerate(result['extracted_sections'][:5], 1):
            print(f"{i}. {section['section_title']}")
            print(f"   Document: {section['document']}")
            print(f"   Page: {section['page_number']} | Score: {section['relevance_score']}")
            print(f"   Type: {section['content_type']} | Words: {section['word_count']}")
            print()
        
        # Diagnostic Information
        print("🔧 DIAGNOSTIC INFORMATION")
        print("-" * 40)
        print(f"Total blocks analyzed: {result['metadata']['total_blocks_analyzed']}")
        print(f"Analysis method: {result['metadata']['analysis_method']}")
        print(f"Processing timestamp: {result['metadata']['processing_timestamp']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return None

def compare_with_original():
    """Compare enhanced results with original results if available"""
    
    output_dir = Path(__file__).parent.parent / "output"
    
    original_file = output_dir / "results.json"
    enhanced_file = output_dir / "enhanced_results.json"
    
    if not original_file.exists():
        print("ℹ️  No original results file found for comparison")
        return
    
    if not enhanced_file.exists():
        print("❌ Enhanced results file not found")
        return
    
    print("\n" + "=" * 60)
    print("🔄 COMPARISON: Original vs Enhanced")
    print("=" * 60)
    
    try:
        with open(original_file, 'r', encoding='utf-8') as f:
            original = json.load(f)
        
        with open(enhanced_file, 'r', encoding='utf-8') as f:
            enhanced = json.load(f)
        
        # Compare personas
        orig_personas = len(original.get('discovered_personas', []))
        enh_personas = len(enhanced.get('discovered_personas', []))
        print(f"👥 Personas: Original={orig_personas}, Enhanced={enh_personas}")
        
        # Compare jobs
        orig_jobs = len(original.get('discovered_jobs', []))
        enh_jobs = len(enhanced.get('discovered_jobs', []))
        print(f"🎯 Jobs: Original={orig_jobs}, Enhanced={enh_jobs}")
        
        # Compare sections
        orig_sections = len(original.get('extracted_sections', []))
        enh_sections = len(enhanced.get('extracted_sections', []))
        print(f"📄 Sections: Original={orig_sections}, Enhanced={enh_sections}")
        
        # Show persona details if available
        if enhanced.get('discovered_personas'):
            print(f"\n✅ Enhanced Analysis Successfully Discovered:")
            for persona in enhanced['discovered_personas']:
                print(f"  - {persona['type']} (confidence: {persona['confidence']:.2f})")
        
        if enhanced.get('discovered_jobs'):
            for job in enhanced['discovered_jobs']:
                print(f"  - {job['type']} (confidence: {job['confidence']:.2f})")
        
    except Exception as e:
        print(f"❌ Error comparing results: {e}")

if __name__ == "__main__":
    # For Adobe Acrobat learning materials, use:
    # PERSONA = "Software Learner"
    # JOB = "Learn Adobe Acrobat features for document management and collaboration"

    # Or alternatively:
    # PERSONA = "Technical Implementer" 
    # JOB = "Master PDF creation, editing, and e-signature workflows"

    # Or for business use:
    # PERSONA = "Business Professional"
    # JOB = "Implement efficient document workflows for team collaboration"
    
    # Run the enhanced analysis
    result = run_enhanced_analysis()
    
    if result:
        # Compare with original if available
        compare_with_original()
        
        print("\n" + "=" * 60)
        print("🎉 Analysis Complete!")
        print("=" * 60)
        print("Next steps:")
        print("1. Check output/enhanced_results.json for detailed results")
        print("2. Review the discovered personas and jobs above")
        print("3. If personas/jobs are still empty, run the diagnostic script")
        print("4. Use docker-run.sh web to view results in browser")
    else:
        print("\n❌ Analysis failed. Please check the error messages above.")
