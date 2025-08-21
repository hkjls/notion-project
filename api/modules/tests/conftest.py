import os
import sys
from pathlib import Path
import django

# Obtenir le chemin racine du projet
root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root))

def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
    django.setup()