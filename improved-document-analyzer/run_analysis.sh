#!/bin/bash

# Run script for the Structural Document Analyzer
# Usage: ./run_analysis.sh

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

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

# Default values
INPUT_DIR="./documents"
OUTPUT_FILE="analysis_results.json"
PERSONA="Travel Planner"
JOB="Plan a trip of 4 days for a group of 10 college friends"

# Function to show usage
show_usage() {
    echo "🔍 Structural Document Analyzer"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -i, --input DIR     Input directory containing PDF files (default: ./documents)"
    echo "  -o, --output FILE   Output JSON file (default: analysis_results.json)"
    echo "  -p, --persona TEXT  User persona description"
    echo "  -j, --job TEXT      Job to be done description"
    echo "  -t, --test          Run test mode with sample data"
    echo "  -h, --help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 -i ./pdfs -p \"Travel Planner\" -j \"Plan a 4-day trip\""
    echo "  $0 --test"
    echo ""
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -i|--input)
            INPUT_DIR="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -p|--persona)
            PERSONA="$2"
            shift 2
            ;;
        -j|--job)
            JOB="$2"
            shift 2
            ;;
        -t|--test)
            print_info "Running test mode..."
            python3 test_analyzer.py
            exit 0
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Main analysis function
run_analysis() {
    print_info "Starting Structural Document Analysis"
    echo "=" * 60
    
    # Check if input directory exists
    if [ ! -d "$INPUT_DIR" ]; then
        print_error "Input directory '$INPUT_DIR' does not exist"
        exit 1
    fi
    
    # Check for PDF files
    pdf_count=$(find "$INPUT_DIR" -name "*.pdf" | wc -l)
    if [ "$pdf_count" -eq 0 ]; then
        print_error "No PDF files found in '$INPUT_DIR'"
        exit 1
    fi
    
    print_info "Found $pdf_count PDF files in $INPUT_DIR"
    print_info "Persona: $PERSONA"
    print_info "Job: $JOB"
    print_info "Output: $OUTPUT_FILE"
    
    # Run the analyzer
    print_info "Running structural analysis..."
    
    if python3 structural_document_analyzer.py \
        --input_dir "$INPUT_DIR" \
        --persona "$PERSONA" \
        --job "$JOB" \
        --output "$OUTPUT_FILE"; then
        
        print_success "Analysis completed successfully!"
        print_info "Results saved to: $OUTPUT_FILE"
        
        # Show summary if jq is available
        if command -v jq &> /dev/null; then
            echo ""
            print_info "Analysis Summary:"
            echo "Documents processed: $(jq -r '.metadata.input_documents | length' "$OUTPUT_FILE")"
            echo "Sections extracted: $(jq -r '.extracted_sections | length' "$OUTPUT_FILE")"
            echo "Subsections analyzed: $(jq -r '.subsection_analysis | length' "$OUTPUT_FILE")"
            
            echo ""
            print_info "Top Sections:"
            jq -r '.extracted_sections[] | "\(.importance_rank). \(.section_title) (\(.document))"' "$OUTPUT_FILE"
        fi
        
    else
        print_error "Analysis failed!"
        exit 1
    fi
}

# Check Python dependencies
check_dependencies() {
    print_info "Checking dependencies..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    # Check for required Python packages
    python3 -c "import PyPDF2, json, re, datetime, collections, math" 2>/dev/null || {
        print_error "Required Python packages are missing"
        print_info "Please install: pip install PyPDF2"
        exit 1
    }
    
    print_success "Dependencies check passed"
}

# Main execution
main() {
    echo "🔍 Structural Document Analyzer for Persona-Driven Intelligence"
    echo "=============================================================="
    
    check_dependencies
    run_analysis
    
    echo ""
    print_success "Analysis complete!"
    echo "Next steps:"
    echo "1. Review the results in $OUTPUT_FILE"
    echo "2. Use the extracted sections for your specific use case"
    echo "3. Run with different persona/job combinations for comparison"
}

# Run main function
main "$@"
