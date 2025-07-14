#!/usr/bin/env python3
"""
Migration script to help transition from monolithic app.py to modular structure.
This script will help you test the new structure without affecting your current workflow.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'langchain', 'langchain-community',
        'sentence-transformers', 'chromadb', 'ctransformers',
        'transformers', 'pydantic'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies found")
    return True

def backup_original_app():
    """Create a backup of the original app.py"""
    if os.path.exists("app.py"):
        backup_path = "app_original_backup.py"
        shutil.copy2("app.py", backup_path)
        print(f"✅ Original app.py backed up as {backup_path}")
        return True
    return False

def test_new_structure():
    """Test the new modular structure"""
    print("🧪 Testing new modular structure...")
    
    try:
        # Test imports
        from config import settings
        from api.models import Query
        from utils.helpers import load_data
        from services.vector_store import VectorStoreService
        from services.rag_service import RAGService
        from services.translation import TranslationService
        from middleware.rate_limiter import RateLimiter
        
        print("✅ All modules import successfully")
        return True
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def run_basic_tests():
    """Run basic functionality tests"""
    print("🧪 Running basic tests...")
    
    try:
        # Test configuration
        from config import settings
        assert settings.persistent_dir == "/data"
        assert settings.search_k == 2
        
        # Test data loading
        from utils.helpers import load_data, validate_qa_pair
        test_data = load_data("data/tourism_faq_gov.json")
        assert len(test_data) > 0
        
        # Test validation
        valid_item = {"question": "Test question?", "answer": "Test answer."}
        assert validate_qa_pair(valid_item) == True
        
        print("✅ Basic tests passed")
        return True
    except Exception as e:
        print(f"❌ Basic tests failed: {e}")
        return False

def main():
    """Main migration process"""
    print("🚀 Starting migration to modular structure...")
    print("=" * 50)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Step 2: Backup original app
    backup_original_app()
    
    # Step 3: Test new structure
    if not test_new_structure():
        print("❌ New structure test failed. Please check the error above.")
        sys.exit(1)
    
    # Step 4: Run basic tests
    if not run_basic_tests():
        print("❌ Basic tests failed. Please check the error above.")
        sys.exit(1)
    
    print("=" * 50)
    print("✅ Migration completed successfully!")
    print("\n📋 Next steps:")
    print("1. Test the new app: python app_refactored.py")
    print("2. If everything works, you can rename app_refactored.py to app.py")
    print("3. Run tests: pytest tests/")
    print("4. Update your Dockerfile if needed")
    print("\n🔄 To revert:")
    print("   - Use app_original_backup.py to restore the original structure")

if __name__ == "__main__":
    main() 