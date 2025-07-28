# PowerShell script to run the auto-adaptive analyzer

Write-Host "🤖 Auto-Adaptive Document Analyzer" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Check if documents directory exists
if (-not (Test-Path "documents")) {
    Write-Host "❌ Documents directory not found" -ForegroundColor Red
    exit 1
}

# Count PDF files
$pdfCount = (Get-ChildItem "documents" -Filter "*.pdf").Count
Write-Host "📁 Found $pdfCount PDF files" -ForegroundColor Green

# Create output directory
New-Item -ItemType Directory -Force -Path "output" | Out-Null

# Run the auto-adaptive analyzer
Write-Host "🚀 Running auto-adaptive analysis..." -ForegroundColor Yellow

docker run -v "${PWD}/documents:/app/documents" -v "${PWD}/output:/app/output" document-analyzer python3 auto_adaptive_analyzer.py --input_dir /app/documents --output /app/output/auto_adaptive_results.json

# Check if results were created
if (Test-Path "output/auto_adaptive_results.json") {
    Write-Host "✅ Analysis completed successfully!" -ForegroundColor Green
    
    # Display results summary
    $results = Get-Content "output/auto_adaptive_results.json" | ConvertFrom-Json
    
    Write-Host "`n📊 RESULTS SUMMARY" -ForegroundColor Cyan
    Write-Host "==================" -ForegroundColor Cyan
    Write-Host "Document Type: $($results.metadata.detected_document_type)" -ForegroundColor White
    Write-Host "Effective Persona: $($results.metadata.effective_persona)" -ForegroundColor White
    Write-Host "Effective Job: $($results.metadata.effective_job)" -ForegroundColor White
    Write-Host "Sections Found: $($results.extracted_sections.Count)" -ForegroundColor White
    
    Write-Host "`n📄 TOP SECTIONS:" -ForegroundColor Cyan
    foreach ($section in $results.extracted_sections) {
        Write-Host "$($section.importance_rank). $($section.section_title)" -ForegroundColor White
        Write-Host "   Document: $($section.document) | Page: $($section.page_number) | Score: $($section.relevance_score)" -ForegroundColor Gray
    }
    
} else {
    Write-Host "❌ Analysis failed - no results file generated" -ForegroundColor Red
}
