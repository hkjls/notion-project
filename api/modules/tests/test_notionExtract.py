from datetime import datetime
import pytest
from ..notion_client import save_task_from_json
# import sys
# from pathlib import Path

# root = Path(__file__).resolve().parent.parent.parent
# sys.path.append(str(root))
from base.models import Task

@pytest.mark.django_db  # Important: permet l'accès à la base de données
def test_save_task_from_json():
    test_data = {
        "tasks": "Create API endpoint",
        "date": "2023-12-01",
        "projects": "Notion Integration",
        "clients": "Example Client",
        "entreprise": "Tech Corp",
        "tech_stack": "Python, Django"
    }
    
    task = save_task_from_json(test_data)
    assert task.tasks == "Create API endpoint"
    assert str(task.date) == "2023-12-01"
    assert task.projects == "Notion Integration"
    assert task.clients == "Example Client"
    assert task.entreprise == "Tech Corp"
    assert task.tech_stack == "Python, Django"
