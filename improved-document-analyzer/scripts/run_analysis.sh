#!/bin/bash

# Enhanced analysis runner script
set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

print_info "Enhanced Adaptive Document Analyzer"
echo "Project root: $PROJECT_ROOT"

# Check if documents exist
if [ ! -d "$PROJECT_ROOT/documents" ] || [ -z "$(ls -A "$PROJECT_ROOT/documents"/*.pdf 2>/dev/null)" ]; then
    print_error "No PDF files found in documents directory"
    exit 1
fi

# Count PDF files
PDF_COUNT=$(ls -1 "$PROJECT_ROOT/documents"/*.pdf 2>/dev/null | wc -l)
print_info "Found $PDF_COUNT PDF files in documents directory"

# Create output directory
mkdir -p "$PROJECT_ROOT/output"

# Check if enhanced analyzer exists
if [ ! -f "$PROJECT_ROOT/enhanced_adaptive_analyzer.py" ]; then
    print_warning "Enhanced analyzer not found. Please ensure enhanced_adaptive_analyzer.py is in the project root."
    exit 1
fi

# Run diagnostic analysis first
print_info "Running diagnostic analysis..."
cd "$PROJECT_ROOT"
python3 scripts/diagnostic_analyzer.py

# Run enhanced analysis
print_info "Running enhanced analysis..."
python3 scripts/run_enhanced_analysis.py

# Check results
if [ -f "$PROJECT_ROOT/output/enhanced_results.json" ]; then
    print_success "Enhanced analysis completed successfully!"
    
    # Show quick summary
    print_info "Quick summary:"
    python3 -c "
import json
with open('output/enhanced_results.json', 'r') as f:
    data = json.load(f)
print(f'Personas discovered: {len(data.get(\"discovered_personas\", []))}')
print(f'Jobs discovered: {len(data.get(\"discovered_jobs\", []))}')
print(f'Sections extracted: {len(data.get(\"extracted_sections\", []))}')
"
else
    print_error "Enhanced analysis failed - no results file generated"
    exit 1
fi

print_success "Analysis complete! Check output/enhanced_results.json for detailed results"
