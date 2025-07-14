# Hura Tourism Chatbot - Project Cleanup Plan

## 🎯 **Current State Analysis**

### **Files to Keep (Production)**

- `app.py` - Main production application
- `config.py` - Configuration settings
- `requirements.txt` - Dependencies
- `Dockerfile` - Container configuration
- `.dockerignore` - Docker exclusions
- `README.md` - Project documentation

### **Files to Organize**

- `services/` - Service modules
- `api/` - API models
- `middleware/` - Middleware components
- `utils/` - Utility functions
- `tests/` - Test files
- `static/` - Web interface files
- `data/` - Data files

### **Files to Archive/Remove**

- Multiple app versions (app_enhanced.py, app_menu_based.py, etc.)
- Backup files (app_backup.py, app_original_backup.py)
- Multiple test files scattered in root
- Documentation files that can be consolidated

## 📁 **Proposed Clean Structure**

```
hura-chatbot/
├── README.md                    # Main documentation
├── app.py                       # Production application
├── config.py                    # Configuration
├── requirements.txt             # Dependencies
├── Dockerfile                   # Container config
├── .dockerignore               # Docker exclusions
├── .gitignore                  # Git exclusions
├── .gitattributes              # Git attributes
│
├── services/                    # Core services
│   ├── __init__.py
│   ├── rag_service.py          # RAG functionality
│   ├── translation.py          # Translation service
│   ├── vector_store.py         # Vector database
│   ├── maps_service.py         # Maps integration
│   └── weather_service.py      # Weather integration
│
├── api/                        # API components
│   ├── __init__.py
│   └── models.py               # Pydantic models
│
├── middleware/                  # Middleware
│   ├── __init__.py
│   └── rate_limiter.py         # Rate limiting
│
├── utils/                      # Utilities
│   ├── __init__.py
│   └── helpers.py              # Helper functions
│
├── tests/                      # All test files
│   ├── __init__.py
│   ├── test_api.py             # API tests
│   ├── test_translations.py    # Translation tests
│   ├── test_deployed.py        # Deployment tests
│   └── test_integration.py     # Integration tests
│
├── static/                     # Web interface
│   ├── index.html              # Main interface
│   └── deployed_interface.html # Deployed version
│
├── data/                       # Data files
│   ├── local_blog_etiquette.json
│   ├── tourism_faq_gov.json
│   └── tripadvisor_forum.json
│
├── docs/                       # Documentation
│   ├── DEPLOYMENT.md           # Deployment guide
│   ├── API_REFERENCE.md        # API documentation
│   ├── FEATURES.md             # Feature overview
│   └── SETUP.md                # Setup instructions
│
├── scripts/                    # Utility scripts
│   ├── migrate.py              # Data migration
│   └── deploy.py               # Deployment script
│
└── archive/                    # Archived files
    ├── app_enhanced.py         # Enhanced version
    ├── app_menu_based.py       # Menu-based version
    ├── app_backup.py           # Backup files
    └── old_tests/              # Old test files
```

## 🧹 **Cleanup Actions**

### **1. Create Organized Directories**

- Move all test files to `tests/`
- Consolidate documentation in `docs/`
- Archive old versions in `archive/`
- Organize scripts in `scripts/`

### **2. Consolidate Documentation**

- Merge multiple README files
- Create comprehensive API documentation
- Consolidate setup guides

### **3. Clean Up Test Files**

- Remove duplicate tests
- Organize by functionality
- Keep only essential tests

### **4. Archive Old Versions**

- Move experimental versions to archive
- Keep only production-ready code
- Document what each archived version was for

### **5. Update Main Files**

- Clean up main app.py
- Update README with current status
- Ensure all imports work with new structure

## 🚀 **Benefits of Cleanup**

1. **Professional Structure** - Industry-standard organization
2. **Easy Maintenance** - Clear separation of concerns
3. **Better Documentation** - Consolidated and organized
4. **Cleaner Repository** - No clutter or confusion
5. **Easier Onboarding** - New developers can understand quickly

## 📋 **Implementation Steps**

1. Create new directory structure
2. Move files to appropriate locations
3. Update imports and paths
4. Test everything still works
5. Update documentation
6. Remove unnecessary files
7. Commit clean structure

Would you like me to proceed with this cleanup?
