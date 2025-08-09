#!/usr/bin/env python3
"""
Hybrid Policy Analyzer with Pinecone + Gemini
Uses Pinecone for vector search and Gemini for answer generation.
"""

import tempenv
import os
import requests
import time
import json
from pathlib import Path
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

class HybridPolicyAnalyzer:
    """Hybrid analyzer using Pinecone for search and Gemini for answers."""
    
    def __init__(self):
        """Initialize the hybrid system."""
        self.setup_gemini()
        self.setup_pinecone()
        self.setup_embeddings()
        
    def setup_gemini(self):
        """Setup Gemini configuration."""
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        genai.configure(api_key=api_key)
        self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        print("✅ Gemini configured successfully")
    
    def setup_pinecone(self):
        """Setup Pinecone configuration."""
        api_key = os.environ.get('PINECONE_API_KEY')
        environment = os.environ.get('PINECONE_ENVIRONMENT')
        index_name = os.environ.get('PINECONE_INDEX_NAME')
        
        if not all([api_key, environment, index_name]):
            raise ValueError("Pinecone configuration incomplete")
        
        try:
            # Initialize Pinecone with new API
            self.pc = Pinecone(api_key=api_key)
            self.index = self.pc.Index(index_name)
            print(f"✅ Pinecone connected to index: {index_name}")
        except Exception as e:
            print(f"❌ Pinecone connection failed: {e}")
            raise
    
    def setup_embeddings(self):
        """Setup sentence transformers for embeddings."""
        model_name = os.environ.get('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
        self.embedding_model = SentenceTransformer(model_name)
        print(f"✅ Embedding model loaded: {model_name}")
    
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
        """Extract text from PDF and chunk it."""
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text_chunks = []
                
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    # Split into smaller chunks (500-800 characters each)
                    chunks = self.chunk_text(page_text, max_length=600)
                    
                    for i, chunk in enumerate(chunks):
                        chunk_id = f"page_{page_num+1}_chunk_{i+1}"
                        text_chunks.append({
                            'id': chunk_id,
                            'text': chunk,
                            'page': page_num + 1,
                            'chunk': i + 1
                        })
                
                return text_chunks
        except Exception as e:
            print(f"❌ Error reading PDF: {e}")
            return []
    
    def chunk_text(self, text, max_length=600):
        """Split text into chunks."""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 > max_length and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def upload_to_pinecone(self, text_chunks):
        """Upload text chunks to Pinecone with embeddings."""
        print(f"📤 Uploading {len(text_chunks)} chunks to Pinecone...")
        
        vectors = []
        for chunk in text_chunks:
            # Generate embedding
            embedding = self.embedding_model.encode(chunk['text']).tolist()
            
            # Create vector record
            vector = {
                'id': chunk['id'],
                'values': embedding,
                'metadata': {
                    'text': chunk['text'],
                    'page': chunk['page'],
                    'chunk': chunk['chunk']
                }
            }
            vectors.append(vector)
        
        try:
            # Upsert vectors in batches
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)
                print(f"✅ Uploaded batch {i//batch_size + 1}/{(len(vectors)-1)//batch_size + 1}")
            
            print(f"✅ Successfully uploaded {len(vectors)} chunks to Pinecone")
            return True
        except Exception as e:
            print(f"❌ Error uploading to Pinecone: {e}")
            return False
    
    def search_relevant_chunks(self, question, top_k=5):
        """Search for relevant chunks using Pinecone."""
        try:
            # Generate embedding for the question
            question_embedding = self.embedding_model.encode(question).tolist()
            
            # Search in Pinecone
            results = self.index.query(
                vector=question_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            relevant_chunks = []
            for match in results.matches:
                relevant_chunks.append({
                    'text': match.metadata['text'],
                    'page': match.metadata['page'],
                    'chunk': match.metadata['chunk'],
                    'score': match.score
                })
            
            return relevant_chunks
        except Exception as e:
            print(f"❌ Error searching Pinecone: {e}")
            return []
    
    def answer_with_gemini(self, question, relevant_chunks):
        """Generate answer using Gemini with relevant chunks."""
        if not relevant_chunks:
            return "No relevant information found in the document."
        
        # Prepare context from relevant chunks
        context = "\n\n".join([
            f"Page {chunk['page']}, Chunk {chunk['chunk']} (Relevance: {chunk['score']:.3f}):\n{chunk['text']}"
            for chunk in relevant_chunks
        ])
        
        prompt = f"""
You are an expert insurance policy analyst. Answer the following question based ONLY on the provided document excerpts.

Question: {question}

Relevant Document Excerpts:
{context}

Instructions:
1. Answer the question based ONLY on the provided excerpts
2. If the information is not in the excerpts, state "Information not found in the provided document excerpts"
3. Be specific and accurate
4. Include page numbers when referencing information
5. If multiple excerpts contain relevant information, synthesize them

Answer:
"""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Error generating answer: {e}"
    
    def analyze_policy(self, pdf_url, questions):
        """Complete policy analysis workflow."""
        print("🤖 Starting Hybrid Policy Analysis")
        print("=" * 50)
        
        # Download PDF
        pdf_filename = self.download_pdf(pdf_url)
        if not pdf_filename:
            return None
        
        try:
            # Extract and chunk text
            print("📖 Extracting and chunking text...")
            text_chunks = self.extract_pdf_text(pdf_filename)
            
            if not text_chunks:
                print("❌ No text content found in PDF")
                return None
            
            print(f"✅ Created {len(text_chunks)} text chunks")
            
            # Upload to Pinecone
            if not self.upload_to_pinecone(text_chunks):
                print("❌ Failed to upload to Pinecone")
                return None
            
            # Answer questions
            print(f"\n🔍 Answering {len(questions)} questions...")
            answers = []
            
            for i, question in enumerate(questions, 1):
                print(f"\n📋 Question {i}/{len(questions)}: {question}")
                
                # Search for relevant chunks
                relevant_chunks = self.search_relevant_chunks(question, top_k=3)
                
                if relevant_chunks:
                    print(f"✅ Found {len(relevant_chunks)} relevant chunks")
                    
                    # Generate answer
                    answer = self.answer_with_gemini(question, relevant_chunks)
                    answers.append({
                        'question': question,
                        'answer': answer,
                        'relevant_chunks': len(relevant_chunks)
                    })
                else:
                    print("❌ No relevant chunks found")
                    answers.append({
                        'question': question,
                        'answer': "No relevant information found in the document.",
                        'relevant_chunks': 0
                    })
                
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
    """Main function to test the hybrid system."""
    print("🤖 Hybrid Policy Analyzer (Pinecone + Gemini)")
    print("=" * 60)
    
    try:
        # Initialize analyzer
        analyzer = HybridPolicyAnalyzer()
        
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
            print(f"\n📊 ANALYSIS RESULTS:")
            print("=" * 60)
            
            for i, result in enumerate(results, 1):
                print(f"\n## Question {i}: {result['question']}")
                print(f"**Answer:** {result['answer']}")
                print(f"**Relevant Chunks:** {result['relevant_chunks']}")
                print("-" * 50)
            
            # Save results
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            output_file = f"hybrid_analysis_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'document_url': test_query['documents'],
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'results': results
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Analysis saved to: {output_file}")
        
        print(f"\n🎉 Hybrid analysis completed!")
        
    except Exception as e:
        print(f"❌ System error: {e}")

if __name__ == "__main__":
    main()
