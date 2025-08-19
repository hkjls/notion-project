import os
from pathlib import Path
import sys
from django.core.asgi import get_asgi_application
from asgiref.sync import sync_to_async
import asyncio


# Configuration du chemin racine
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

# Configuration de l'environnement Django d'abord
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

# Initialisation de l'application ASGI
application = get_asgi_application()

# Création d'une fonction wrapper pour get_db
from modules.notion_client import get_db

@sync_to_async
def init_db():
    print("Initialisation de la base de données...")
    return get_db("List")

async def periodic_task():
    while True:
        try:
            await init_db()
            await asyncio.sleep(1)  # Attendre 1 seconde
        except Exception as e:
            print(f"Erreur dans periodic_task: {e}")
            await asyncio.sleep(1)  # Continuer même en cas d'erreur

# Démarrer la tâche périodique
asyncio.create_task(periodic_task())