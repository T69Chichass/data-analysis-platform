#!/usr/bin/env python3
"""
Enhanced test script to extract specific information from the National Parivar Mediclaim Plus Policy.
"""
import asyncio
import re
from document_processor import DocumentProcessor
from pathlib import Path

async def extract_specific_info():
    """Extract specific information from the policy document."""
    
    pdf_path = "National_Parivar_Mediclaim_Plus_Policy.pdf"
    
    print("🔍 Extracting specific information from National Parivar Mediclaim Plus Policy...")
    
    try:
        # Extract text from the document
        processor = DocumentProcessor()
        extracted_text = await processor._extract_text_from_pdf(Path(pdf_path))
        
        print(f"📄 Document text length: {len(extracted_text)} characters")
        
        # Define search patterns for specific information
        search_patterns = {
            "grace_period": [
                r"grace period.*?(\d+)\s*days?",
                r"grace.*?(\d+)\s*days?",
                r"premium.*?grace.*?(\d+)",
            ],
            "waiting_period_ped": [
                r"pre-existing.*?(\d+)\s*years?",
                r"PED.*?(\d+)\s*years?",
                r"waiting period.*?pre-existing.*?(\d+)",
            ],
            "maternity": [
                r"maternity.*?covered",
                r"maternity.*?not covered",
                r"pregnancy.*?expenses",
            ],
            "cataract": [
                r"cataract.*?(\d+)\s*years?",
                r"cataract.*?waiting.*?(\d+)",
            ],
            "organ_donor": [
                r"organ donor.*?covered",
                r"donor.*?expenses",
                r"transplant.*?donor",
            ],
            "ncd": [
                r"No Claim Discount.*?(\d+)%",
                r"NCD.*?(\d+)%",
                r"no claim.*?(\d+)",
            ],
            "preventive_health": [
                r"preventive.*?health",
                r"health check.*?covered",
                r"annual.*?check.*?up",
            ],
            "hospital_definition": [
                r"Hospital.*?(\d+)\s*beds?",
                r"hospital.*?defined.*?(\d+)",
                r"registered.*?hospital",
            ],
            "ayush": [
                r"AYUSH.*?(\d+)%",
                r"ayush.*?(\d+)",
                r"alternative.*?medicine",
            ],
            "room_rent": [
                r"room rent.*?(\d+)%",
                r"ICU.*?(\d+)%",
                r"sub-limit.*?room",
            ]
        }
        
        # Search for each pattern
        results = {}
        
        for category, patterns in search_patterns.items():
            print(f"\n--- Searching for {category.replace('_', ' ').title()} ---")
            found_matches = []
            
            for pattern in patterns:
                matches = re.findall(pattern, extracted_text, re.IGNORECASE)
                if matches:
                    found_matches.extend(matches)
                    print(f"   ✅ Found: {matches}")
            
            if not found_matches:
                # Try broader search
                category_keywords = {
                    "grace_period": ["grace", "premium", "payment"],
                    "waiting_period_ped": ["pre-existing", "PED", "waiting"],
                    "maternity": ["maternity", "pregnancy", "delivery"],
                    "cataract": ["cataract", "eye", "surgery"],
                    "organ_donor": ["organ", "donor", "transplant"],
                    "ncd": ["no claim", "NCD", "discount"],
                    "preventive_health": ["preventive", "health check", "annual"],
                    "hospital_definition": ["hospital", "beds", "registered"],
                    "ayush": ["AYUSH", "ayurveda", "alternative"],
                    "room_rent": ["room rent", "ICU", "sub-limit"]
                }
                
                keywords = category_keywords.get(category, [])
                for keyword in keywords:
                    if keyword.lower() in extracted_text.lower():
                        # Find the context around the keyword
                        text_lower = extracted_text.lower()
                        keyword_pos = text_lower.find(keyword.lower())
                        if keyword_pos != -1:
                            start = max(0, keyword_pos - 100)
                            end = min(len(extracted_text), keyword_pos + 200)
                            context = extracted_text[start:end]
                            print(f"   📄 Found keyword '{keyword}' in context: {context[:150]}...")
                            found_matches.append(f"Keyword '{keyword}' found")
                            break
            
            results[category] = found_matches
        
        # Generate comprehensive report
        print("\n" + "="*60)
        print("📋 COMPREHENSIVE POLICY ANALYSIS REPORT")
        print("="*60)
        
        for category, matches in results.items():
            print(f"\n🔍 {category.replace('_', ' ').title()}:")
            if matches:
                for match in matches[:3]:  # Show first 3 matches
                    print(f"   ✅ {match}")
            else:
                print("   ❌ No specific information found")
        
        print("\n" + "="*60)
        print("✅ Analysis completed!")
        
        return results
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(extract_specific_info())
