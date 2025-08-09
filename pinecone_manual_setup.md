# 🌲 Pinecone Setup Guide

## Step 1: Get Your Pinecone API Key

1. Go to [Pinecone Console](https://app.pinecone.io)
2. Sign up or log in to your account
3. Go to **API Keys** section
4. Copy your API key (starts with `pcsk_`)

## Step 2: Create a New Index

1. In Pinecone Console, click **Create Index**
2. Fill in the details:
   - **Name**: `loopers1`
   - **Dimensions**: `384` (for all-MiniLM-L6-v2 model)
   - **Metric**: `cosine`
   - **Cloud**: Choose your preferred cloud (AWS, GCP, or Azure)
   - **Region**: Choose a region close to you

## Step 3: Note Your Environment

After creating the index, note down:
- **Index Name**: `loopers1`
- **Environment**: This will be shown in the index details (e.g., `gcp-starter`, `us-east-1`, etc.)

## Step 4: Update Your Configuration

Update your `tempenv.py` file with the correct values:

```python
# Set environment variables for the session
os.environ['PINECONE_API_KEY'] = 'your_actual_api_key_here'
os.environ['PINECONE_ENVIRONMENT'] = 'your_actual_environment_here'  # e.g., 'gcp-starter'
os.environ['PINECONE_INDEX_NAME'] = 'loopers1'
```

## Step 5: Test the Connection

Run the test script:
```bash
python check_credits.py
```

## Common Environment Names

- **GCP Starter**: `gcp-starter`
- **AWS US East**: `us-east-1`
- **AWS US West**: `us-west1-gcp`
- **Azure**: `eastus-azure`

## Troubleshooting

### If you get "Index not found" error:
1. Check that the index name in `tempenv.py` matches exactly
2. Verify the environment name is correct
3. Make sure the index is fully initialized (can take a few minutes)

### If you get "Invalid API key" error:
1. Verify your API key starts with `pcsk_`
2. Make sure you copied the entire key
3. Check that your Pinecone account is active

### If you get network errors:
1. Check your internet connection
2. Try using a different network
3. Check if your firewall is blocking the connection

## Quick Test

After setup, run this to test:
```bash
python test_api_connection.py
```

You should see:
- ✅ Pinecone Manager: Working
- ✅ Gemini Manager: Working
- ✅ All services configured and working
