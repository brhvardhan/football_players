import asyncio
import sys
from fastapi.testclient import TestClient
from main import app

if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

client = TestClient(app)

def test_get_average():
    response = client.get("/team/average_age")
    assert response.status_code == 200