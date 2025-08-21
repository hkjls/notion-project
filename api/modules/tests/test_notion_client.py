import pytest
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root))
from modules.notion_client import get_db

@pytest.mark.django_db
def test_get_db():
    result = get_db("List")