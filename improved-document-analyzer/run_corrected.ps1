# PowerShell script to run the corrected analyzer

Write-Host "🔧 Corrected Adobe Acrobat Document Analyzer" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# Check if documents directory exists
if (-not (Test-Path "documents")) {
    Write-Host "❌ Documents directory not found" -ForegroundColor Red
    exit 1
}

# Count PDF files
$pdfCount = (Get-ChildItem "documents" -Filter "*.pdf").Count
Write-Host "📁 Found $pdfCount Adobe Acrobat PDF files" -ForegroundColor Green

# Create output directory
New-Item -ItemType Directory -Force -Path "output" | Out-Null

# Run the corrected analyzer
Write-Host "`n🚀 Running corrected analysis with proper Adobe Acrobat persona-job..." -ForegroundColor Yellow

docker run -v "${PWD}/documents:/app/documents" -v "${PWD}/output:/app/output" document-analyzer python3 scripts/run_corrected_analysis.py

# Check if results were created
if (Test-Path "output/corrected_adobe_results.json") {
    Write-Host "✅ Corrected analysis completed successfully!" -ForegroundColor Green
    
    # Display results summary
    try {
        $results = Get-Content "output/corrected_adobe_results.json" | ConvertFrom-Json
        
        Write-Host "`n📊 CORRECTED RESULTS SUMMARY" -ForegroundColor Cyan
        Write-Host "=============================" -ForegroundColor Cyan
        Write-Host "✅ Persona: $($results.metadata.persona)" -ForegroundColor Green
        Write-Host "✅ Job: $($results.metadata.job_to_be_done)" -ForegroundColor Green
        Write-Host "📄 Documents: $($results.metadata.input_documents.Count)" -ForegroundColor White
        Write-Host "📋 Sections: $($results.extracted_sections.Count)" -ForegroundColor White
        
        Write-Host "`n📄 TOP ADOBE ACROBAT SECTIONS:" -ForegroundColor Cyan
        foreach ($section in $results.extracted_sections) {
            Write-Host "$($section.importance_rank). $($section.section_title)" -ForegroundColor White
            Write-Host "   📁 $($section.document) | 📄 Page $($section.page_number)" -ForegroundColor Gray
        }
        
        # Check if persona was actually corrected
        if ($results.metadata.persona -ne "Travel Planner") {
            Write-Host "`n🎉 SUCCESS: Persona correctly updated to Adobe Acrobat workflow!" -ForegroundColor Green
        } else {
            Write-Host "`n⚠️  WARNING: Persona still shows Travel Planner - may need deeper fix" -ForegroundColor Yellow
        }
        
    } catch {
        Write-Host "⚠️  Results created but couldn't parse summary" -ForegroundColor Yellow
    }
    
} else {
    Write-Host "❌ Corrected analysis failed - no results file generated" -ForegroundColor Red
}
