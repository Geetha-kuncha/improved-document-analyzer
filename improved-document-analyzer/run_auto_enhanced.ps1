# PowerShell script to run the auto-enhanced analyzer

Write-Host "🤖 Auto-Enhanced Document Analyzer" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan

# Check if documents directory exists
if (-not (Test-Path "documents")) {
    Write-Host "❌ Documents directory not found" -ForegroundColor Red
    Write-Host "💡 Please create a 'documents' directory and add your PDF files" -ForegroundColor Yellow
    exit 1
}

# Count PDF files
$pdfFiles = Get-ChildItem "documents" -Filter "*.pdf"
$pdfCount = $pdfFiles.Count

if ($pdfCount -eq 0) {
    Write-Host "❌ No PDF files found in documents directory" -ForegroundColor Red
    Write-Host "💡 Please add PDF files to the 'documents' directory" -ForegroundColor Yellow
    exit 1
}

Write-Host "📁 Found $pdfCount PDF files:" -ForegroundColor Green
foreach ($file in $pdfFiles) {
    Write-Host "  - $($file.Name)" -ForegroundColor Gray
}

# Create output directory
New-Item -ItemType Directory -Force -Path "output" | Out-Null

# Run the auto-enhanced analyzer
Write-Host "`n🚀 Running auto-enhanced analysis..." -ForegroundColor Yellow

try {
    docker run -v "${PWD}/documents:/app/documents" -v "${PWD}/output:/app/output" document-analyzer python3 scripts/run_enhanced_auto_analysis.py
    
    # Check if results were created
    if (Test-Path "output/auto_enhanced_results.json") {
        Write-Host "✅ Analysis completed successfully!" -ForegroundColor Green
        
        # Display results summary
        try {
            $results = Get-Content "output/auto_enhanced_results.json" | ConvertFrom-Json
            
            Write-Host "`n📊 RESULTS SUMMARY" -ForegroundColor Cyan
            Write-Host "==================" -ForegroundColor Cyan
            Write-Host "Persona Used: $($results.metadata.persona)" -ForegroundColor White
            Write-Host "Job Used: $($results.metadata.job_to_be_done)" -ForegroundColor White
            Write-Host "Documents Processed: $($results.metadata.input_documents.Count)" -ForegroundColor White
            Write-Host "Sections Found: $($results.extracted_sections.Count)" -ForegroundColor White
            
            Write-Host "`n📄 TOP SECTIONS:" -ForegroundColor Cyan
            foreach ($section in $results.extracted_sections) {
                Write-Host "$($section.importance_rank). $($section.section_title)" -ForegroundColor White
                Write-Host "   📁 $($section.document) | 📄 Page $($section.page_number)" -ForegroundColor Gray
            }
            
            Write-Host "`n🎉 SUCCESS: Auto-detection and analysis completed!" -ForegroundColor Green
            Write-Host "💡 Check output/auto_enhanced_results.json for full details" -ForegroundColor Yellow
            
        } catch {
            Write-Host "⚠️  Results file created but couldn't parse summary" -ForegroundColor Yellow
            Write-Host "💡 Check output/auto_enhanced_results.json manually" -ForegroundColor Yellow
        }
        
    } else {
        Write-Host "❌ Analysis failed - no results file generated" -ForegroundColor Red
        Write-Host "💡 Check the Docker container logs for error details" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ Error running Docker container: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Make sure Docker is running and the document-analyzer image exists" -ForegroundColor Yellow
}

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
