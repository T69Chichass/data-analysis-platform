#!/bin/bash
echo "🧹 Cleaning previous installations..."
pip uninstall -y fastapi uvicorn pydantic

echo "📦 Installing Flask dependencies..."
pip install Flask==2.2.3 Flask-CORS==3.0.10 requests==2.28.1 PyPDF2==3.0.1

echo "✅ Build completed successfully!"
