#!/usr/bin/env python3
"""
Enhanced Policy Analyzer with Full Accuracy
Uses comprehensive document processing and multiple search strategies.
"""

import tempenv
import os
import requests
import time
import json
import re
from pathlib import Path
import google.generativeai as genai

class EnhancedPolicyAnalyzer:
    """Enhanced analyzer for maximum accuracy."""
    
    def __init__(self):
        """Initialize the enhanced system."""
        self.setup_gemini()
        
    def setup_gemini(self):
        """Setup Gemini configuration."""
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        genai.configure(api_key=api_key)
        self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        print("✅ Gemini configured successfully")
    
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
                start = max(0, text_lower.find(keyword.lower()) - 200)
                end = min(len(text), text_lower.find(keyword.lower()) + len(keyword) + 200)
                context = text[start:end]
                results.append({
                    'keyword': keyword,
                    'context': context,
                    'position': text_lower.find(keyword.lower())
                })
        
        return results
    
    def analyze_with_comprehensive_search(self, text, question):
        """Analyze question using comprehensive search strategies."""
        
        # Strategy 1: Direct question analysis
        prompt1 = f"""
You are an expert insurance policy analyst. Analyze this document thoroughly to answer the question.

Question: {question}

Document Content:
{text[:15000]}

Instructions:
1. Search through the ENTIRE document content carefully
2. Look for any information related to the question, even if it's mentioned briefly
3. Check for synonyms and related terms
4. If you find ANY relevant information, provide it
5. If the information is not explicitly mentioned, state "Information not found in the document"
6. Be thorough and comprehensive in your search

Answer:
"""
        
        try:
            response1 = self.gemini_model.generate_content(prompt1)
            answer1 = response1.text
        except Exception as e:
            answer1 = f"Error in analysis: {e}"
        
        # Strategy 2: Keyword-based search
        keywords = self.extract_keywords_from_question(question)
        keyword_results = self.search_keywords_in_text(text, keywords)
        
        if keyword_results:
            keyword_context = "\n\n".join([f"Keyword '{r['keyword']}': {r['context']}" for r in keyword_results])
            
            prompt2 = f"""
Based on the following keyword matches found in the document, answer this question:

Question: {question}

Keyword Matches Found:
{keyword_context}

Instructions:
1. Analyze the keyword matches carefully
2. Extract any relevant information from the context
3. Provide a comprehensive answer based on the found information
4. If the keyword matches don't contain the answer, state "Information not found in the document"

Answer:
"""
            
            try:
                response2 = self.gemini_model.generate_content(prompt2)
                answer2 = response2.text
            except Exception as e:
                answer2 = f"Error in keyword analysis: {e}"
        else:
            answer2 = "No keyword matches found"
        
        # Strategy 3: Section-by-section analysis
        sections = self.split_into_sections(text)
        section_answers = []
        
        for i, section in enumerate(sections[:5]):  # Analyze first 5 sections
            prompt3 = f"""
Analyze this section of the insurance policy document for information related to this question:

Question: {question}

Section {i+1}:
{section[:3000]}

Instructions:
1. Look for any information related to the question
2. If found, provide the specific details
3. If not found, respond with "No relevant information in this section"

Answer:
"""
            
            try:
                response3 = self.gemini_model.generate_content(prompt3)
                if "No relevant information" not in response3.text:
                    section_answers.append(f"Section {i+1}: {response3.text}")
            except Exception as e:
                continue
        
        # Combine all strategies
        combined_answer = f"""
COMPREHENSIVE ANALYSIS:

Direct Analysis:
{answer1}

Keyword Analysis:
{answer2}

Section Analysis:
{chr(10).join(section_answers) if section_answers else "No relevant information found in sections"}

FINAL ANSWER:
"""
        
        # Generate final comprehensive answer
        final_prompt = f"""
Based on the comprehensive analysis above, provide a clear, accurate answer to this question:

Question: {question}

Analysis Results:
{combined_answer}

Instructions:
1. Synthesize all the information from the analysis
2. Provide the most accurate and complete answer possible
3. If any information was found, include it
4. If no information was found, clearly state "Information not found in the document"
5. Be specific and detailed

Final Answer:
"""
        
        try:
            final_response = self.gemini_model.generate_content(final_prompt)
            return final_response.text
        except Exception as e:
            return f"Error generating final answer: {e}"
    
    def extract_keywords_from_question(self, question):
        """Extract relevant keywords from the question."""
        keywords = []
        
        # Common insurance terms
        insurance_terms = [
            'grace period', 'premium', 'payment', 'waiting period', 'pre-existing',
            'diseases', 'maternity', 'expenses', 'cataract', 'surgery', 'organ donor',
            'medical expenses', 'no claim discount', 'ncd', 'preventive', 'health check',
            'hospital', 'ayush', 'room rent', 'icu', 'charges', 'sub-limits', 'plan a'
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
    
    def split_into_sections(self, text):
        """Split text into logical sections."""
        # Split by common section markers
        section_markers = [
            'SECTION', 'CHAPTER', 'CLAUSE', 'ARTICLE', 'DEFINITION',
            'COVERAGE', 'EXCLUSIONS', 'CONDITIONS', 'GENERAL CONDITIONS'
        ]
        
        sections = []
        current_section = ""
        
        lines = text.split('\n')
        for line in lines:
            if any(marker in line.upper() for marker in section_markers):
                if current_section:
                    sections.append(current_section)
                current_section = line
            else:
                current_section += "\n" + line
        
        if current_section:
            sections.append(current_section)
        
        return sections if sections else [text]
    
    def analyze_policy(self, pdf_url, questions):
        """Complete enhanced policy analysis workflow."""
        print("🤖 Starting Enhanced Policy Analysis for Maximum Accuracy")
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
            
            # Answer questions with enhanced analysis
            print(f"\n🔍 Analyzing {len(questions)} questions with enhanced accuracy...")
            answers = []
            
            for i, question in enumerate(questions, 1):
                print(f"\n📋 Question {i}/{len(questions)}: {question}")
                print("🔍 Performing comprehensive analysis...")
                
                # Enhanced analysis
                answer = self.analyze_with_comprehensive_search(text, question)
                
                answers.append({
                    'question': question,
                    'answer': answer
                })
                
                print(f"✅ Analysis completed for question {i}")
                
                # Small delay between questions
                time.sleep(1)
            
            return answers
            
        finally:
            # Clean up
            try:
                os.remove(pdf_filename)
                print(f"🧹 Cleaned up: {pdf_filename}")
            except:
                pass

def main():
    """Main function to test the enhanced system."""
    print("🤖 Enhanced Policy Analyzer for Maximum Accuracy")
    print("=" * 60)
    
    try:
        # Initialize analyzer
        analyzer = EnhancedPolicyAnalyzer()
        
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
            print(f"\n📊 ENHANCED ANALYSIS RESULTS:")
            print("=" * 60)
            
            for i, result in enumerate(results, 1):
                print(f"\n## Question {i}: {result['question']}")
                print(f"**Answer:** {result['answer']}")
                print("-" * 50)
            
            # Save results
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            output_file = f"enhanced_analysis_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'document_url': test_query['documents'],
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'results': results
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Enhanced analysis saved to: {output_file}")
        
        print(f"\n🎉 Enhanced analysis completed!")
        
    except Exception as e:
        print(f"❌ System error: {e}")

if __name__ == "__main__":
    main()
