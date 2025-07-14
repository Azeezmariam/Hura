#!/usr/bin/env python3
"""
Deployment helper for enhanced Hura Tourism Chatbot
Guides you through updating your Hugging Face Space
"""

import os
import shutil
import subprocess
from pathlib import Path

def check_files():
    """Check if all required files are present"""
    print("🔍 Checking required files...")
    
    required_files = [
        "app_menu_based.py",
        "config.py", 
        "requirements.txt",
        "api/models_enhanced.py",
        "services/maps_service.py",
        "services/weather_service.py",
        "services/rag_service.py",
        "services/translation.py",
        "services/vector_store.py",
        "middleware/rate_limiter.py",
        "utils/helpers.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required files present")
        return True

def backup_current_app():
    """Backup the current app.py"""
    if os.path.exists("app.py"):
        print("📦 Backing up current app.py...")
        shutil.copy("app.py", "app_backup.py")
        print("✅ Backup created: app_backup.py")
        return True
    else:
        print("⚠️ No app.py found to backup")
        return False

def deploy_enhanced_version():
    """Deploy the enhanced menu-based version"""
    print("🚀 Deploying enhanced version...")
    
    try:
        # Copy menu-based app to main app
        shutil.copy("app_menu_based.py", "app.py")
        print("✅ app_menu_based.py copied to app.py")
        
        # Ensure all directories exist
        directories = ["api", "services", "middleware", "utils", "data"]
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"✅ Created directory: {directory}")
        
        print("✅ Enhanced version ready for deployment")
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

def check_git_status():
    """Check git status and provide deployment instructions"""
    print("\n📋 Git Status Check...")
    
    try:
        # Check if this is a git repository
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Git repository found")
            
            # Check for changes
            if "Changes not staged for commit" in result.stdout:
                print("📝 Changes detected - ready to commit")
                print("\n📋 Next steps:")
                print("1. git add .")
                print("2. git commit -m 'Deploy enhanced menu-based chatbot'")
                print("3. git push")
                print("4. Wait 2-5 minutes for Hugging Face deployment")
                
            elif "nothing to commit" in result.stdout:
                print("✅ No changes to commit")
                
        else:
            print("⚠️ Not a git repository or git not available")
            print("📋 Manual deployment required:")
            print("1. Upload files to Hugging Face Space")
            print("2. Replace app.py with app_menu_based.py")
            print("3. Ensure all directories and files are present")
            
    except FileNotFoundError:
        print("⚠️ Git not found - manual deployment required")
        print("📋 Manual deployment steps:")
        print("1. Go to https://huggingface.co/spaces/lola9/hura-chatbot")
        print("2. Upload or replace files")
        print("3. Replace app.py with app_menu_based.py")
        print("4. Wait for deployment")

def verify_api_keys():
    """Verify API keys are configured"""
    print("\n🔑 API Keys Verification...")
    
    # Check if API keys are in environment or config
    api_keys = {
        "GOOGLE_MAPS_API_KEY": os.getenv("GOOGLE_MAPS_API_KEY"),
        "OPENWEATHER_API_KEY": os.getenv("OPENWEATHER_API_KEY")
    }
    
    print("📋 API Keys Status:")
    for key_name, key_value in api_keys.items():
        if key_value:
            print(f"   ✅ {key_name}: Configured")
        else:
            print(f"   ⚠️ {key_name}: Not found in environment")
    
    print("\n💡 Note: API keys should be set as Hugging Face Secrets")
    print("   - Go to your Space settings")
    print("   - Add secrets: GOOGLE_MAPS_API_KEY and OPENWEATHER_API_KEY")

def create_deployment_summary():
    """Create a deployment summary"""
    print("\n📊 DEPLOYMENT SUMMARY")
    print("=" * 50)
    
    print("✅ Enhanced Features Ready:")
    print("   - Menu-based interface")
    print("   - Google Maps integration")
    print("   - Weather forecasting")
    print("   - Enhanced translation")
    print("   - Tourism information")
    
    print("\n🎯 New Endpoints:")
    print("   - GET /menu - Main menu")
    print("   - POST /maps - Location services")
    print("   - POST /weather - Weather information")
    print("   - POST /ask - Enhanced questions")
    print("   - POST /translate/* - Translation services")
    
    print("\n🚀 After Deployment:")
    print("   - Test with: python3 test_enhanced_deployed.py")
    print("   - Monitor Hugging Face logs")
    print("   - Check API key functionality")

def main():
    """Main deployment function"""
    print("🚀 Enhanced Hura Tourism Chatbot Deployment Helper")
    print("=" * 60)
    
    # Check files
    if not check_files():
        print("❌ Cannot proceed - missing required files")
        return
    
    # Backup current app
    backup_current_app()
    
    # Deploy enhanced version
    if not deploy_enhanced_version():
        print("❌ Deployment failed")
        return
    
    # Check git status
    check_git_status()
    
    # Verify API keys
    verify_api_keys()
    
    # Create summary
    create_deployment_summary()
    
    print("\n🎉 Deployment helper completed!")
    print("📋 Follow the instructions above to complete deployment")

if __name__ == "__main__":
    main() 