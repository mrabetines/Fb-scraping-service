import pytest
from httpx import AsyncClient

from main import app



@pytest.mark.anyio
async def test_endpoint():

    async with AsyncClient(app=app) as ac:
        response = await ac.post("http://localhost:8000/scraping/posts?url=houwaida.haute.couture")
    assert response.status_code == 200
    str.__contains__(str(response.content), "finished scrapping")