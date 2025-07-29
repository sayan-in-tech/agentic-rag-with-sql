import os
import shutil
from pathlib import Path

def clean_pycache():
    """
    Recursively removes all __pycache__ directories in the project.
    """
    project_root = Path(__file__).parent.parent.parent
    for root, dirs, files in os.walk(project_root):
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(cache_dir)
            except Exception as e:
                print(f"Error cleaning {cache_dir}: {str(e)}") 

    print("Cache cleaned successfully")