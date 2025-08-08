# Configuration Guide

This guide will help you configure the external services for full functionality.

## Current Status

Your application is currently running in **mock mode** with the following services:
- ✅ **Application**: Running successfully on http://localhost:8000
- 🔄 **Pinecone**: Mock mode (no vector search)
- 🔄 **OpenAI**: Mock mode (no AI responses)
- ✅ **Database**: Mock SQLite (working)
- ✅ **Embedding Model**: Working

## Step 1: Configure Pinecone (Vector Database)

### 1.1 Get Pinecone Account
1. Sign up at [pinecone.io](https://pinecone.io)
2. Create a new project
3. Get your API key from the dashboard

### 1.2 Create Pinecone Index
1. In your Pinecone dashboard, create a new index:
   - **Name**: `insurance-policy-index` (or your preferred name)
   - **Dimensions**: `384` (for the current embedding model)
   - **Metric**: `cosine`
   - **Environment**: Note your environment (e.g., `gcp-starter`)

### 1.3 Update Configuration
Edit `dependencies.py` and update the PineconeManager `__init__` method:

```python
# Replace these placeholder values:
self.api_key = os.getenv("PINECONE_API_KEY", "your_actual_api_key_here")
self.index_name = os.getenv("PINECONE_INDEX_NAME", "your_actual_index_name_here")
self.environment = os.getenv("PINECONE_ENVIRONMENT", "your_actual_environment_here")
```

## Step 2: Configure OpenAI

### 2.1 Get OpenAI API Key
1. Sign up at [openai.com](https://openai.com)
2. Get your API key from the dashboard

### 2.2 Update Configuration
Edit `dependencies.py` and update the OpenAIManager `__init__` method:

```python
# Replace this placeholder value:
self.api_key = os.getenv("OPENAI_API_KEY", "your_actual_openai_api_key_here")
```

## Step 3: Test Configuration

After updating the configuration, restart the application:

```bash
python main.py
```

Then test the health endpoint:
```bash
curl http://localhost:8000/health
```

You should see:
- `pinecone`: `healthy` (instead of `mock_mode`)
- `openai`: `healthy` (instead of `mock_mode`)

## Step 4: Upload Documents

Once Pinecone is configured, you can upload documents for vector search:

```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Content-Type: application/json" \
  -d '{
    "document_type": "insurance_policy",
    "content": "Your document content here..."
  }'
```

## Step 5: Query Documents

Test the full functionality:

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the coverage amount?",
    "document_type": "insurance_policy"
  }'
```

## Troubleshooting

### Pinecone Issues
- **Index not found**: Make sure your index name matches exactly
- **Dimensions mismatch**: Ensure your index has 384 dimensions
- **API key invalid**: Check your Pinecone API key

### OpenAI Issues
- **API key invalid**: Check your OpenAI API key
- **Rate limits**: Check your OpenAI usage limits

### Database Issues
- The application currently uses SQLite in mock mode
- For production, configure PostgreSQL using the environment variables

## Environment Variables (Optional)

If you prefer using environment variables, create a `.env` file:

```bash
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX_NAME=your_pinecone_index_name
OPENAI_API_KEY=your_openai_api_key
```

Then uncomment the `load_dotenv()` line in `dependencies.py`.
