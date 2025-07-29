import os
import shutil

def clean_pycache():
    """Clean all __pycache__ directories"""
    try:
        for root, dirs, files in os.walk('.'):
            for dir_name in dirs:
                if dir_name == '__pycache__':
                    cache_path = os.path.join(root, dir_name)
                    shutil.rmtree(cache_path)
                    
        print("Cache cleaned successfully")
    except Exception as e:
        print(f"❌ [utils/cache_cleaner.py:clean_pycache] Error cleaning cache: {str(e)}")