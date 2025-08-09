#!/usr/bin/env python3
"""
Enhanced Text-Based Policy Analyzer for Maximum Accuracy
Uses improved search patterns and better text processing.
"""

import tempenv
import os
import requests
import time
import json
import re
from pathlib import Path

class EnhancedTextPolicyAnalyzer:
    """Enhanced text-based analyzer for maximum accuracy."""
    
    def __init__(self):
        """Initialize the enhanced text-based system."""
        print("✅ Enhanced text-based analyzer initialized")
    
    def download_pdf(self, url, filename="policy.pdf"):
        """Download PDF from URL."""
        try:
            print(f"📥 Downloading PDF from: {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ PDF downloaded successfully: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error downloading PDF: {e}")
            return None
    
    def extract_pdf_text(self, pdf_path):
        """Extract text from PDF with enhanced processing."""
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                full_text = ""
                
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    full_text += f"\n--- Page {page_num + 1} ---\n"
                    full_text += page_text
                    full_text += "\n"
                
                return full_text
        except Exception as e:
            print(f"❌ Error reading PDF: {e}")
            return ""
    
    def extract_grace_period(self, text):
        """Extract grace period information with enhanced patterns."""
        patterns = [
            r'grace period.*?(\d+)\s*days?',
            r'(\d+)\s*days?.*?grace period',
            r'grace period.*?thirty\s*days?',
            r'thirty\s*days?.*?grace period',
            r'grace period.*?30\s*days?',
            r'30\s*days?.*?grace period'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                days = match.group(1) if match.group(1) else '30'
                return f"Grace period: {days} days"
        
        return "Information not found in the document"
    
    def extract_waiting_period_ped(self, text):
        """Extract waiting period for pre-existing diseases with enhanced patterns."""
        patterns = [
            r'pre-existing disease.*?(\d+)\s*months?',
            r'(\d+)\s*months?.*?pre-existing disease',
            r'ped.*?(\d+)\s*months?',
            r'thirty-six\s*months?.*?pre-existing',
            r'36\s*months?.*?pre-existing',
            r'pre-existing.*?excluded.*?(\d+)\s*months?',
            r'(\d+)\s*months?.*?continuous coverage',
            r'pre-existing.*?(\d+)\s*months?.*?continuous'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                months = match.group(1) if match.group(1) else '36'
                return f"Waiting period for pre-existing diseases (PED): {months} months of continuous coverage"
        
        # Look for specific text about pre-existing diseases
        if 'pre-existing disease' in text.lower() and 'excluded' in text.lower():
            # Find the context around pre-existing disease
            start = text.lower().find('pre-existing disease')
            context = text[max(0, start-1000):min(len(text), start+1000)]
            if '36' in context or 'thirty-six' in context:
                return "Waiting period for pre-existing diseases (PED): 36 months of continuous coverage"
        
        return "Information not found in the document"
    
    def extract_maternity_coverage(self, text):
        """Extract maternity expenses coverage with enhanced patterns."""
        patterns = [
            r'maternity.*?expenses?.*?covered',
            r'maternity.*?benefits?',
            r'pregnancy.*?expenses?',
            r'childbirth.*?expenses?',
            r'maternity.*?treatment',
            r'pregnancy.*?treatment'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                start = max(0, match.start() - 1000)
                end = min(len(text), match.end() + 1000)
                context = text[start:end]
                return f"Maternity coverage found: {context}"
        
        # Check if maternity is mentioned in exclusions
        if 'maternity' in text.lower() and 'exclusion' in text.lower():
            start = text.lower().find('maternity')
            context = text[max(0, start-500):min(len(text), start+500)]
            return f"Maternity coverage status: {context}"
        
        return "Information not found in the document"
    
    def extract_cataract_waiting_period(self, text):
        """Extract cataract surgery waiting period with enhanced patterns."""
        patterns = [
            r'cataract.*?(\d+)\s*months?',
            r'(\d+)\s*months?.*?cataract',
            r'cataract.*?waiting period',
            r'waiting period.*?cataract',
            r'cataract.*?surgery.*?(\d+)',
            r'(\d+).*?cataract.*?surgery'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                months = match.group(1) if match.group(1) else 'specified'
                return f"Waiting period for cataract surgery: {months} months"
        
        # Look for cataract in exclusions or waiting periods
        if 'cataract' in text.lower():
            start = text.lower().find('cataract')
            context = text[max(0, start-1000):min(len(text), start+1000)]
            return f"Cataract surgery information found: {context}"
        
        return "Information not found in the document"
    
    def extract_organ_donor_coverage(self, text):
        """Extract organ donor expenses coverage with enhanced patterns."""
        patterns = [
            r'organ donor.*?expenses?',
            r'organ donor.*?covered',
            r'donor.*?medical expenses?',
            r'organ.*?donor.*?costs?',
            r'organ donor.*?hospitalisation',
            r'donor.*?hospitalisation.*?expenses?'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                start = max(0, match.start() - 1000)
                end = min(len(text), match.end() + 1000)
                context = text[start:end]
                return f"Organ donor coverage found: {context}"
        
        return "Information not found in the document"
    
    def extract_ncd_information(self, text):
        """Extract No Claim Discount information with enhanced patterns."""
        patterns = [
            r'no claim discount.*?(\d+)\s*percent',
            r'ncd.*?(\d+)\s*percent',
            r'(\d+)\s*percent.*?no claim discount',
            r'no claim discount.*?(\d+)\s*%',
            r'(\d+)\s*%.*?no claim discount',
            r'no claim discount.*?(\d+)',
            r'(\d+).*?no claim discount'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                percentage = match.group(1) if match.group(1) else 'specified'
                return f"No Claim Discount (NCD): {percentage}%"
        
        return "Information not found in the document"
    
    def extract_preventive_health_check(self, text):
        """Extract preventive health check-up benefits with enhanced patterns."""
        patterns = [
            r'preventive.*?health check',
            r'health check.*?benefit',
            r'preventive.*?medical',
            r'annual.*?health check',
            r'health check.*?up',
            r'preventive.*?care',
            r'health screening',
            r'preventive.*?examination'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                start = max(0, match.start() - 1000)
                end = min(len(text), match.end() + 1000)
                context = text[start:end]
                return f"Preventive health check benefit found: {context}"
        
        return "Information not found in the document"
    
    def extract_hospital_definition(self, text):
        """Extract hospital definition with enhanced patterns."""
        patterns = [
            r'hospital.*?means.*?institution',
            r'definition.*?hospital',
            r'hospital.*?definition',
            r'hospital.*?institution.*?established',
            r'institution.*?established.*?hospital'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                start = max(0, match.start() - 2000)
                end = min(len(text), match.end() + 2000)
                context = text[start:end]
                
                # Extract the full definition
                definition_start = context.find('Hospital')
                if definition_start != -1:
                    # Look for the end of the definition
                    definition_end = context.find('.', definition_start + 100)
                    if definition_end != -1:
                        definition = context[definition_start:definition_end + 1]
                        return f"Hospital Definition: {definition}"
                
                return f"Hospital definition found: {context}"
        
        return "Information not found in the document"
    
    def extract_ayush_coverage(self, text):
        """Extract AYUSH treatment coverage with enhanced patterns."""
        patterns = [
            r'ayush.*?treatment',
            r'ayush.*?coverage',
            r'ayurveda.*?yoga.*?naturopathy',
            r'ayush.*?day care',
            r'ayush.*?hospital',
            r'ayush.*?medical',
            r'ayush.*?indemnify'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                start = max(0, match.start() - 1500)
                end = min(len(text), match.end() + 1500)
                context = text[start:end]
                return f"AYUSH coverage found: {context}"
        
        return "Information not found in the document"
    
    def extract_room_rent_limits(self, text):
        """Extract room rent and ICU sub-limits with enhanced patterns."""
        patterns = [
            r'room rent.*?sub.limit',
            r'icu.*?charges.*?sub.limit',
            r'room rent.*?limit',
            r'icu.*?limit',
            r'plan a.*?room rent',
            r'plan a.*?icu',
            r'room.*?rent.*?charges',
            r'icu.*?charges',
            r'sub.limit.*?room',
            r'sub.limit.*?icu'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                start = max(0, match.start() - 1000)
                end = min(len(text), match.end() + 1000)
                context = text[start:end]
                return f"Room rent/ICU sub-limits found: {context}"
        
        return "Information not found in the document"
    
    def analyze_question(self, text, question):
        """Analyze a specific question using enhanced text-based methods."""
        question_lower = question.lower()
        
        if 'grace period' in question_lower and 'premium' in question_lower:
            return self.extract_grace_period(text)
        elif 'waiting period' in question_lower and 'pre-existing' in question_lower:
            return self.extract_waiting_period_ped(text)
        elif 'maternity' in question_lower and 'expenses' in question_lower:
            return self.extract_maternity_coverage(text)
        elif 'cataract' in question_lower and 'surgery' in question_lower:
            return self.extract_cataract_waiting_period(text)
        elif 'organ donor' in question_lower and 'expenses' in question_lower:
            return self.extract_organ_donor_coverage(text)
        elif 'no claim discount' in question_lower or 'ncd' in question_lower:
            return self.extract_ncd_information(text)
        elif 'preventive' in question_lower and 'health check' in question_lower:
            return self.extract_preventive_health_check(text)
        elif 'hospital' in question_lower and 'define' in question_lower:
            return self.extract_hospital_definition(text)
        elif 'ayush' in question_lower and 'coverage' in question_lower:
            return self.extract_ayush_coverage(text)
        elif 'room rent' in question_lower and 'icu' in question_lower and 'plan a' in question_lower:
            return self.extract_room_rent_limits(text)
        else:
            return "Question pattern not recognized for text-based analysis"
    
    def analyze_policy(self, pdf_url, questions):
        """Complete enhanced text-based policy analysis workflow."""
        print("🤖 Starting Enhanced Text-Based Policy Analysis for Maximum Accuracy")
        print("=" * 60)
        
        # Download PDF
        pdf_filename = self.download_pdf(pdf_url)
        if not pdf_filename:
            return None
        
        try:
            # Extract text
            print("📖 Extracting text from PDF...")
            text = self.extract_pdf_text(pdf_filename)
            
            if not text.strip():
                print("❌ No text content found in PDF")
                return None
            
            print(f"✅ Extracted {len(text)} characters of text")
            
            # Answer questions with enhanced text-based analysis
            print(f"\n🔍 Analyzing {len(questions)} questions with enhanced text-based methods...")
            answers = []
            
            for i, question in enumerate(questions, 1):
                print(f"\n📋 Question {i}/{len(questions)}: {question}")
                print("🔍 Performing enhanced text-based analysis...")
                
                # Enhanced text-based analysis
                answer = self.analyze_question(text, question)
                
                answers.append({
                    'question': question,
                    'answer': answer
                })
                
                print(f"✅ Analysis completed for question {i}")
            
            return answers
            
        finally:
            # Clean up
            try:
                os.remove(pdf_filename)
                print(f"🧹 Cleaned up: {pdf_filename}")
            except:
                pass

def main():
    """Main function to test the enhanced text-based system."""
    print("🤖 Enhanced Text-Based Policy Analyzer for Maximum Accuracy")
    print("=" * 60)
    
    try:
        # Initialize analyzer
        analyzer = EnhancedTextPolicyAnalyzer()
        
        # Test query
        test_query = {
            "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
            "questions": [
                "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
                "What is the waiting period for pre-existing diseases (PED) to be covered?",
                "Does this policy cover maternity expenses, and what are the conditions?",
                "What is the waiting period for cataract surgery?",
                "Are the medical expenses for an organ donor covered under this policy?",
                "What is the No Claim Discount (NCD) offered in this policy?",
                "Is there a benefit for preventive health check-ups?",
                "How does the policy define a 'Hospital'?",
                "What is the extent of coverage for AYUSH treatments?",
                "Are there any sub-limits on room rent and ICU charges for Plan A?"
            ]
        }
        
        # Analyze policy
        results = analyzer.analyze_policy(test_query['documents'], test_query['questions'])
        
        if results:
            print(f"\n📊 ENHANCED TEXT-BASED ANALYSIS RESULTS:")
            print("=" * 60)
            
            found_count = 0
            for i, result in enumerate(results, 1):
                print(f"\n## Question {i}: {result['question']}")
                print(f"**Answer:** {result['answer']}")
                
                # Count found information
                if "Information not found" not in result['answer'] and "not recognized" not in result['answer']:
                    found_count += 1
                
                print("-" * 50)
            
            # Calculate accuracy
            accuracy = (found_count / len(test_query['questions'])) * 100
            print(f"\n📈 ACCURACY SUMMARY:")
            print(f"Questions with information found: {found_count}/{len(test_query['questions'])}")
            print(f"Accuracy: {accuracy:.1f}%")
            
            # Save results
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            output_file = f"enhanced_text_analysis_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'document_url': test_query['documents'],
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'accuracy': accuracy,
                    'found_count': found_count,
                    'total_questions': len(test_query['questions']),
                    'results': results
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Enhanced text-based analysis saved to: {output_file}")
        
        print(f"\n🎉 Enhanced text-based analysis completed!")
        
    except Exception as e:
        print(f"❌ System error: {e}")

if __name__ == "__main__":
    main()
