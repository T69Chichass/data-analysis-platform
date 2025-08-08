#!/usr/bin/env python3
"""
Simple database table creation script for SQLite.
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class QueryLog(Base):
    """Model for logging query requests and responses."""
    
    __tablename__ = "query_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    query_id = Column(String(50), unique=True, nullable=False, index=True)
    query_text = Column(Text, nullable=False)
    user_id = Column(String(100), nullable=True, index=True)
    
    # Timing information
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processing_time = Column(Float, nullable=True)
    embedding_time = Column(Float, nullable=True)
    search_time = Column(Float, nullable=True)
    llm_time = Column(Float, nullable=True)
    
    # Result information
    success = Column(Boolean, nullable=False, default=False)
    results_count = Column(Integer, nullable=True)
    confidence_level = Column(String(10), nullable=True)
    
    # Response data
    answer = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    error_code = Column(String(50), nullable=True)

class DocumentMetadata(Base):
    """Model for storing document metadata."""
    
    __tablename__ = "document_metadata"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(100), unique=True, nullable=False, index=True)
    
    # Document information
    title = Column(String(500), nullable=True)
    document_type = Column(String(50), nullable=True, index=True)
    category = Column(String(100), nullable=True, index=True)
    subcategory = Column(String(100), nullable=True)
    
    # File information
    filename = Column(String(255), nullable=True)
    file_path = Column(String(1000), nullable=True)
    file_size = Column(Integer, nullable=True)
    
    # Processing information
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)
    chunk_count = Column(Integer, nullable=True)
    
    # Status
    processing_status = Column(String(20), default="pending", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

class DocumentChunk(Base):
    """Model for storing document chunks and their metadata."""
    
    __tablename__ = "document_chunks"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    chunk_id = Column(String(100), unique=True, nullable=False, index=True)
    document_id = Column(String(100), nullable=False, index=True)
    
    # Chunk information
    chunk_text = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    chunk_size = Column(Integer, nullable=False)
    
    # Context information
    page_number = Column(Integer, nullable=True)
    section_title = Column(String(500), nullable=True)
    section_type = Column(String(50), nullable=True)
    
    # Processing information
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    embedding_generated = Column(Boolean, default=False, nullable=False)
    pinecone_id = Column(String(100), nullable=True, unique=True)

def create_tables(engine):
    """Create all tables."""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    # Create SQLite database
    engine = create_engine('sqlite:///demo.db')
    create_tables(engine)
    print("✅ Database tables created successfully!")
