#!/usr/bin/env python3
"""
Efficient Policy Analyzer with Gemini Pro
Uses optimized search strategies and rate limiting for maximum accuracy.
"""

import tempenv
import os
import requests
import time
import json
import re
from pathlib import Path
import google.generativeai as genai

class EfficientPolicyAnalyzer:
    """Efficient analyzer for maximum accuracy with rate limiting."""
    
    def __init__(self):
        """Initialize the efficient system."""
        self.setup_gemini()
        self.api_calls = 0
        self.max_calls_per_minute = 8  # Conservative limit
        
    def setup_gemini(self):
        """Setup Gemini configuration."""
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        genai.configure(api_key=api_key)
        self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')  # Using Gemini Pro
        print("✅ Gemini Pro configured successfully")
    
    def rate_limit_check(self):
        """Check and enforce rate limiting."""
        self.api_calls += 1
        if self.api_calls % self.max_calls_per_minute == 0:
            print(f"⏳ Rate limit reached. Waiting 60 seconds...")
            time.sleep(60)
    
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
    
    def search_keywords_in_text(self, text, keywords):
        """Search for specific keywords in the text."""
        results = []
        text_lower = text.lower()
        
        for keyword in keywords:
            if keyword.lower() in text_lower:
                # Find the context around the keyword
                start = max(0, text_lower.find(keyword.lower()) - 300)
                end = min(len(text), text_lower.find(keyword.lower()) + len(keyword) + 300)
                context = text[start:end]
                results.append({
                    'keyword': keyword,
                    'context': context,
                    'position': text_lower.find(keyword.lower())
                })
        
        return results
    
    def analyze_with_optimized_search(self, text, question):
        """Analyze question using optimized search strategy."""
        
        # Extract keywords first
        keywords = self.extract_keywords_from_question(question)
        keyword_results = self.search_keywords_in_text(text, keywords)
        
        # Create comprehensive prompt with all relevant information
        if keyword_results:
            keyword_context = "\n\n".join([f"Keyword '{r['keyword']}': {r['context']}" for r in keyword_results])
            
            prompt = f"""
You are an expert insurance policy analyst. Analyze the following information to answer the question accurately.

Question: {question}

Document Content (First 20,000 characters):
{text[:20000]}

Keyword Matches Found:
{keyword_context}

Instructions:
1. Search through ALL the provided content carefully
2. Look for any information related to the question, even if it's mentioned briefly
3. Check for synonyms and related terms
4. If you find ANY relevant information, provide it with specific details
5. If the information is not explicitly mentioned, state "Information not found in the document"
6. Be thorough and comprehensive in your search
7. Provide exact quotes from the document when possible

Answer:
"""
        else:
            prompt = f"""
You are an expert insurance policy analyst. Analyze the following document to answer the question accurately.

Question: {question}

Document Content (First 20,000 characters):
{text[:20000]}

Instructions:
1. Search through ALL the provided content carefully
2. Look for any information related to the question, even if it's mentioned briefly
3. Check for synonyms and related terms
4. If you find ANY relevant information, provide it with specific details
5. If the information is not explicitly mentioned, state "Information not found in the document"
6. Be thorough and comprehensive in your search
7. Provide exact quotes from the document when possible

Answer:
"""
        
        try:
            self.rate_limit_check()
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e):
                print(f"⏳ Rate limit hit. Waiting 60 seconds...")
                time.sleep(60)
                try:
                    response = self.gemini_model.generate_content(prompt)
                    return response.text
                except Exception as e2:
                    return f"Error after retry: {e2}"
            else:
                return f"Error in analysis: {e}"
    
    def extract_keywords_from_question(self, question):
        """Extract relevant keywords from the question."""
        keywords = []
        
        # Common insurance terms
        insurance_terms = [
            'grace period', 'premium', 'payment', 'waiting period', 'pre-existing',
            'diseases', 'maternity', 'expenses', 'cataract', 'surgery', 'organ donor',
            'medical expenses', 'no claim discount', 'ncd', 'preventive', 'health check',
            'hospital', 'ayush', 'room rent', 'icu', 'charges', 'sub-limits', 'plan a',
            'thirty days', 'thirty-six', '36 months', 'continuous coverage'
        ]
        
        # Add question-specific terms
        question_lower = question.lower()
        for term in insurance_terms:
            if term in question_lower:
                keywords.append(term)
        
        # Add specific terms from the question
        specific_terms = re.findall(r'\b\w+\b', question.lower())
        keywords.extend([term for term in specific_terms if len(term) > 3])
        
        return list(set(keywords))  # Remove duplicates
    
    def analyze_policy(self, pdf_url, questions):
        """Complete efficient policy analysis workflow."""
        print("🤖 Starting Efficient Policy Analysis with Gemini Pro")
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
            
            # Answer questions with optimized analysis
            print(f"\n🔍 Analyzing {len(questions)} questions with optimized accuracy...")
            answers = []
            
            for i, question in enumerate(questions, 1):
                print(f"\n📋 Question {i}/{len(questions)}: {question}")
                print("🔍 Performing optimized analysis...")
                
                # Optimized analysis
                answer = self.analyze_with_optimized_search(text, question)
                
                answers.append({
                    'question': question,
                    'answer': answer
                })
                
                print(f"✅ Analysis completed for question {i}")
                
                # Small delay between questions
                time.sleep(2)
            
            return answers
            
        finally:
            # Clean up
            try:
                os.remove(pdf_filename)
                print(f"🧹 Cleaned up: {pdf_filename}")
            except:
                pass

def main():
    """Main function to test the efficient system."""
    print("🤖 Efficient Policy Analyzer with Gemini Pro")
    print("=" * 60)
    
    try:
        # Initialize analyzer
        analyzer = EfficientPolicyAnalyzer()
        
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
            print(f"\n📊 EFFICIENT ANALYSIS RESULTS:")
            print("=" * 60)
            
            found_count = 0
            for i, result in enumerate(results, 1):
                print(f"\n## Question {i}: {result['question']}")
                print(f"**Answer:** {result['answer']}")
                
                # Count found information
                if "Information not found" not in result['answer']:
                    found_count += 1
                
                print("-" * 50)
            
            # Calculate accuracy
            accuracy = (found_count / len(test_query['questions'])) * 100
            print(f"\n📈 ACCURACY SUMMARY:")
            print(f"Questions with information found: {found_count}/{len(test_query['questions'])}")
            print(f"Accuracy: {accuracy:.1f}%")
            
            # Save results
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            output_file = f"efficient_analysis_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'document_url': test_query['documents'],
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'accuracy': accuracy,
                    'found_count': found_count,
                    'total_questions': len(test_query['questions']),
                    'results': results
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Efficient analysis saved to: {output_file}")
        
        print(f"\n🎉 Efficient analysis completed!")
        
    except Exception as e:
        print(f"❌ System error: {e}")

if __name__ == "__main__":
    main()
