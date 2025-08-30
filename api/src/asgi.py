import os
from pathlib import Path
import sys
from django.core.asgi import get_asgi_application
from asgiref.sync import sync_to_async
import asyncio
from functools import lru_cache
from datetime import datetime, timedelta


# Configuration du chemin racine
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

# Configuration de l'environnement Django d'abord
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

# Initialisation de l'application ASGI
application = get_asgi_application()

# Création d'une fonction wrapper pour get_db
from dotenv import load_dotenv
from modules.notion import notion

load_dotenv(f"{root_dir.parent}/.env")
auth = notion(os.getenv('notion_key'))

# Cache pour les résultats (30 secondes)
@lru_cache(maxsize=32)
def cached_get_db(db_name, timestamp):
    return auth.get_db(db_name)

@sync_to_async
def init_db():
    # Utilisation du cache avec timestamp arrondi à la minute
    timestamp = datetime.now().replace(second=0, microsecond=0)
    print(f"[{datetime.now()}] Initialisation de la base de données...")
    return cached_get_db("List", timestamp)

async def periodic_task():
    retry_delay = 1  # Délai initial
    max_retry_delay = 30  # Délai maximum en cas d'erreur
    
    while True:
        try:
            start_time = asyncio.get_event_loop().time()
            await init_db()
            
            # Calcul du temps d'exécution et ajustement du délai
            execution_time = asyncio.get_event_loop().time() - start_time
            sleep_time = max(1 - execution_time, 0)  # Au moins 0 seconde
            
            await asyncio.sleep(sleep_time)
            retry_delay = 1  # Réinitialisation du délai après succès
            
        except Exception as e:
            print(f"[{datetime.now()}] Erreur dans periodic_task: {e}")
            await asyncio.sleep(min(retry_delay, max_retry_delay))
            retry_delay *= 2  # Backoff exponentiel

# Démarrer la tâche périodique avec une meilleure gestion
loop = asyncio.get_event_loop()
task = loop.create_task(periodic_task())