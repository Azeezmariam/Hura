import os
import json
import logging
import sqlite3
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def load_data(path: str) -> List[Dict[str, Any]]:
    """Load JSON data files with improved error handling"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {path}: {e}")
        return []

def validate_qa_pair(item: Dict[str, Any]) -> bool:
    """Validate a question-answer pair"""
    required_fields = ['question', 'answer']
    if not all(field in item for field in required_fields):
        return False
    if len(item['question'].strip()) < 5:
        return False
    if len(item['answer'].strip()) < 10:
        return False
    return True

def deduplicate_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate Q&A pairs based on question content"""
    seen = set()
    unique_data = []
    for item in data:
        if not validate_qa_pair(item):
            continue
        question_hash = hash(item['question'].lower().strip())
        if question_hash not in seen:
            seen.add(question_hash)
            unique_data.append(item)
    return unique_data

def fix_chromadb_schema(db_path: str) -> bool:
    """Fix ChromaDB schema compatibility issues"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if topic column exists
        cursor.execute("PRAGMA table_info(collections)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'topic' not in columns:
            logger.info("Fixing ChromaDB schema...")
            # Add missing columns
            cursor.execute("ALTER TABLE collections ADD COLUMN topic TEXT")
            cursor.execute("ALTER TABLE collections ADD COLUMN dimensionality INTEGER")
            conn.commit()
        
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Schema fix failed: {e}")
        return False

def get_dir_size(path: Path) -> int:
    """Calculate directory size in bytes"""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(Path(entry.path))
    except (PermissionError, FileNotFoundError):
        logger.warning(f"Cannot access directory: {path}")
    return total

def ensure_directories(*paths: Path) -> None:
    """Ensure directories exist, create if they don't"""
    for path in paths:
        try:
            path.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            logger.warning(f"Skipping creation of {path} - already exists") 