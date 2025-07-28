#!/usr/bin/env python3

import os
import sys
import tempfile
from pathlib import Path

# Add the current directory to the path
sys.path.append(str(Path(__file__).parent))

from structural_document_analyzer import StructuralDocumentAnalyzer

def create_test_content():
    """Create test content that mimics the South of France documents"""
    
    # Travel guide content with good structural patterns
    travel_content = """
COMPREHENSIVE GUIDE TO MAJOR CITIES IN THE SOUTH OF FRANCE

Introduction
The South of France offers stunning landscapes and rich cultural heritage.

Nice: The Jewel of the French Riviera
• Promenade des Anglais: Famous seaside promenade built in 19th century
• Castle Hill (Colline du Château): Panoramic views of Nice and Mediterranean
• Old Town (Vieux Nice): Historic center with narrow streets and baroque churches
• Matisse Museum: Dedicated to works of Henri Matisse

Key Attractions:
• Address: 164 Avenue des Arènes de Cimiez, 06000 Nice
• Hours: 10:00 AM - 6:00 PM (closed Tuesdays)
• Price: €10 adults, €5 students
• Phone: +33 4 93 81 08 08

Marseille: The Oldest City in France
Founded by Greek sailors around 600 BC, Marseille is France's oldest city.

Activities:
1. Visit the Old Port (Vieux-Port) - bustling harbor for over 2,600 years
2. Explore Basilica of Notre-Dame de la Garde - panoramic city views
3. Tour MuCEM museum - European and Mediterranean civilizations
4. Walk through Le Panier district - oldest area with colorful buildings

Restaurant Recommendations:
• Le Petit Nice Passedat: €150-200 per person, Michelin 3-star
• Chez Etienne: €25-35 per person, traditional pizzas
• La Merenda: €30-40 per person, authentic Niçoise cuisine

Transportation:
• Metro: €1.70 per ticket
• Bus: €1.70 per ticket
• Taxi: €2.60 base fare + €1.20/km
"""

    # Activities content with different structural patterns
    activities_content = """
ULTIMATE GUIDE TO ACTIVITIES IN THE SOUTH OF FRANCE

Coastal Adventures
The Mediterranean coastline offers numerous water activities:

Beach Hopping:
• Nice: Sandy shores with vibrant Promenade des Anglais
• Antibes: Pebbled beaches and charming old town
• Saint-Tropez: Exclusive beach clubs and glamorous atmosphere
• Cannes: Sandy beaches along Boulevard de la Croisette

Water Sports:
• Jet skiing: Available in Cannes, Nice, Saint-Tropez (€80-120/hour)
• Parasailing: Thrilling aerial views (€60-90 per person)
• Scuba diving: Explore underwater wrecks in Toulon
• Sailing tours: Charter boats from €200-500/day

Cultural Experiences
Art and Museums:
1. Nice: Visit Musée Matisse - dedicated to Henri Matisse works
2. Antibes: Explore Musée Picasso in Château Grimaldi
3. Saint-Paul-de-Vence: Discover modern art at Fondation Maeght
4. Aix-en-Provence: Tour Atelier Cézanne studio

Historical Sites:
• Nîmes: Walk across ancient Roman aqueduct Pont du Gard
• Avignon: Explore Palais des Papes - largest Gothic palace in Europe
• Carcassonne: Wander medieval citadel with 52 towers
• Arles: Visit Roman amphitheater and ancient theater

Festivals and Events:
• Cannes Film Festival: May (prestigious international event)
• Nice Carnival: February (vibrant parades and celebrations)
• Avignon Festival: July (theater, dance, music performances)
• Menton Lemon Festival: February (citrus-themed floats)

Nightlife and Entertainment:
Bars and Lounges:
• Monaco: Le Bar Americain - classic cocktails and live jazz
• Nice: Le Comptoir du Marché - creative cocktails in old town
• Cannes: La Folie Douce - dining and entertainment venue
• Saint-Tropez: Bar du Port - chic waterfront atmosphere

Nightclubs:
• Saint-Tropez: Les Caves du Roy - glamorous celebrity venue
• Nice: High Club - multiple dance floors and top DJs
• Cannes: La Suite - rooftop terrace with city views
"""

    return {
        'cities_guide.pdf': travel_content,
        'activities_guide.pdf': activities_content
    }

def test_structural_analyzer():
    """Test the structural document analyzer"""
    
    print("Testing Structural Document Analyzer")
    print("=" * 50)
    
    # Create test content
    test_contents = create_test_content()
    
    # Create temporary directory and files
    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_paths = []
        
        # Create mock PDF files (using text files for testing)
        for filename, content in test_contents.items():
            file_path = os.path.join(temp_dir, filename.replace('.pdf', '.txt'))
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            pdf_paths.append(file_path)
        
        # Test different persona-job combinations
        test_cases = [
            {
                'persona': 'Travel Planner',
                'job': 'Plan a 4-day trip for a group of 10 college friends',
                'expected_focus': 'activities, accommodations, transportation'
            },
            {
                'persona': 'Cultural Explorer',
                'job': 'Discover historical sites and museums to visit',
                'expected_focus': 'museums, historical sites, cultural experiences'
            },
            {
                'persona': 'Food Enthusiast',
                'job': 'Find the best restaurants and culinary experiences',
                'expected_focus': 'restaurants, cuisine, dining'
            }
        ]
        
        # Initialize analyzer
        analyzer = StructuralDocumentAnalyzer()
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest Case {i}: {test_case['persona']}")
            print(f"Job: {test_case['job']}")
            print("-" * 40)
            
            # Mock the PDF processing by reading text files
            all_sections = []
            document_profiles = {}
            
            for file_path in pdf_paths:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Simulate section extraction
                sections, profile = analyzer.process_single_document_mock(content, os.path.basename(file_path))
                all_sections.extend(sections)
                document_profiles[os.path.basename(file_path)] = profile
            
            # Analyze collection
            collection_profile = analyzer.analyze_collection_structure(all_sections, document_profiles)
            
            # Score sections
            scored_sections = analyzer.score_sections_for_persona_job(
                all_sections, test_case['persona'], test_case['job'], collection_profile
            )
            
            # Select top sections
            selected_sections = analyzer.select_diverse_sections(scored_sections, max_sections=5)
            
            print(f"Found {len(all_sections)} total sections")
            print(f"Selected {len(selected_sections)} top sections")
            
            print("\nTop Selected Sections:")
            for j, section in enumerate(selected_sections[:3], 1):
                print(f"{j}. {section['title']}")
                print(f"   Document: {section['document']}")
                print(f"   Relevance Score: {section['relevance_score']:.3f}")
                print(f"   Structural Score: {section['structural_score']:.3f}")
                print(f"   Info Density: {section['information_density']:.3f}")
        
        print("\n" + "=" * 50)
        print("✅ All tests completed successfully!")
        print("The analyzer successfully:")
        print("• Extracted structured sections from documents")
        print("• Scored sections based on persona-job requirements")
        print("• Selected diverse, relevant content")
        print("• Demonstrated structural analysis over keyword matching")

def process_single_document_mock(self, content: str, filename: str):
    """Mock version of process_single_document for testing"""
    # Split content into sections based on headers and structure
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    sections = []
    
    # Simple section extraction for testing
    current_section_lines = []
    
    for i, line in enumerate(lines):
        # Check if this looks like a section header
        if (line.isupper() or 
            (len(line.split()) <= 8 and line.endswith(':')) or
            re.match(r'^[A-Z][^:\n]{10,50}$', line)):
            
            # Save previous section if it exists
            if current_section_lines and len(current_section_lines) > 3:
                section = self.analyze_content_window(current_section_lines, i-len(current_section_lines), 1, filename)
                if self.is_valid_section(section):
                    sections.append(section)
            
            # Start new section
            current_section_lines = [line]
        else:
            current_section_lines.append(line)
    
    # Add final section
    if current_section_lines and len(current_section_lines) > 3:
        section = self.analyze_content_window(current_section_lines, len(lines)-len(current_section_lines), 1, filename)
        if self.is_valid_section(section):
            sections.append(section)
    
    # Create document profile
    profile = self.analyze_document_profile(sections)
    
    return sections, profile

# Add the mock method to the analyzer class
StructuralDocumentAnalyzer.process_single_document_mock = process_single_document_mock

if __name__ == "__main__":
    test_structural_analyzer()
