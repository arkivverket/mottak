import pytest
from app.main import get_service_url


@pytest.mark.asyncio
async def test_get_service_url():
    account = 'test_account'
    resp = await get_service_url(account)
    assert resp.startswith('https://')
    assert account in resp
