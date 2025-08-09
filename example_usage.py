#!/usr/bin/env python3
"""
Example usage of tempenv.py for accessing API keys and configuration.
This demonstrates how to use the centralized configuration system.
"""

from tempenv import temp_env, get_pinecone_config, get_openai_config, get_database_config

def example_pinecone_usage():
    """Example of using Pinecone configuration."""
    print("🌲 Pinecone Configuration Example:")
    
    # Method 1: Direct access
    api_key = temp_env.PINECONE_API_KEY
    environment = temp_env.PINECONE_ENVIRONMENT
    index_name = temp_env.PINECONE_INDEX_NAME
    
    print(f"   API Key: {api_key[:10]}..." if api_key != 'your_pinecone_api_key' else "   API Key: NOT SET")
    print(f"   Environment: {environment}")
    print(f"   Index Name: {index_name}")
    
    # Method 2: Using convenience function
    pinecone_config = get_pinecone_config()
    print(f"   Config Dict: {pinecone_config}")

def example_openai_usage():
    """Example of using OpenAI configuration."""
    print("\n🤖 OpenAI Configuration Example:")
    
    # Method 1: Direct access
    api_key = temp_env.OPENAI_API_KEY
    model = temp_env.OPENAI_MODEL
    max_tokens = temp_env.OPENAI_MAX_TOKENS
    temperature = temp_env.OPENAI_TEMPERATURE
    
    print(f"   API Key: {api_key[:10]}..." if api_key != 'your_openai_api_key_here' else "   API Key: NOT SET")
    print(f"   Model: {model}")
    print(f"   Max Tokens: {max_tokens}")
    print(f"   Temperature: {temperature}")
    
    # Method 2: Using convenience function
    openai_config = get_openai_config()
    print(f"   Config Dict: {openai_config}")

def example_database_usage():
    """Example of using database configuration."""
    print("\n🗄️ Database Configuration Example:")
    
    # Method 1: Direct access
    host = temp_env.POSTGRES_HOST
    port = temp_env.POSTGRES_PORT
    user = temp_env.POSTGRES_USER
    password = temp_env.POSTGRES_PASSWORD
    database = temp_env.POSTGRES_DB
    
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   User: {user}")
    print(f"   Password: {'*' * len(password) if password != 'your_password_here' else 'NOT SET'}")
    print(f"   Database: {database}")
    
    # Method 2: Using convenience function
    db_config = get_database_config()
    print(f"   Database URL: {db_config['url']}")

def example_validation():
    """Example of validating configuration."""
    print("\n✅ Configuration Validation Example:")
    
    validation = temp_env.validate_required_keys()
    
    for service, keys in validation.items():
        status = "✅" if all(keys.values()) else "❌"
        print(f"   {service.capitalize()}: {status}")
        
        if not all(keys.values()):
            missing = [key for key, valid in keys.items() if not valid]
            print(f"      Missing: {', '.join(missing)}")

def example_application_config():
    """Example of using application configuration."""
    print("\n⚙️ Application Configuration Example:")
    
    print(f"   Environment: {temp_env.APP_ENV}")
    print(f"   Debug Mode: {temp_env.DEBUG}")
    print(f"   Log Level: {temp_env.LOG_LEVEL}")
    print(f"   Embedding Model: {temp_env.EMBEDDING_MODEL}")
    print(f"   Rate Limit: {temp_env.RATE_LIMIT_REQUESTS_PER_MINUTE} requests/minute")
    print(f"   Allowed Hosts: {temp_env.get_allowed_hosts_list()}")

def main():
    """Main function demonstrating all usage examples."""
    print("🚀 tempenv.py Usage Examples")
    print("=" * 50)
    
    # Show configuration summary
    temp_env.print_configuration_summary()
    
    # Demonstrate different usage patterns
    example_pinecone_usage()
    example_openai_usage()
    example_database_usage()
    example_validation()
    example_application_config()
    
    print("\n📝 How to use in your code:")
    print("""
# Import the configuration
from tempenv import temp_env

# Use directly
openai_key = temp_env.OPENAI_API_KEY
pinecone_key = temp_env.PINECONE_API_KEY

# Or use convenience functions
from tempenv import get_openai_config, get_pinecone_config
openai_config = get_openai_config()
pinecone_config = get_pinecone_config()

# Validate configuration
validation = temp_env.validate_required_keys()
if not all(validation['openai'].values()):
    print("OpenAI configuration incomplete!")
    """)

if __name__ == "__main__":
    main()
