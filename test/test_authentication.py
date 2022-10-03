import dbm

import pytest
from requests import Request

from welkin.authentication import DB_PATH, WelkinAuth


@pytest.fixture
def auth(client):
    auth = client.auth
    if auth.tenant != "gh":
        auth.tenant = "test_tenant"
    auth.token_method = lambda: {"token": "API_TOKEN"}

    return auth


def test_auth_eq():
    auth_params = {
        "tenant": "tenant",
        "api_client": "api_client",
        "secret_key": "secret_key",
        "token_method": print,
    }

    auth_1 = WelkinAuth(**auth_params)
    auth_2 = WelkinAuth(**auth_params)

    assert id(auth_1) != id(auth_2)
    assert auth_1 == auth_2


def test_token_get(auth):
    token = auth.token

    assert token is not None
    assert dbm.whichdb(DB_PATH) is not None


def test_token_refresh(auth):
    token = f"{auth.token}_1"
    auth.refresh_token()

    assert token != auth.token


def test_auth_call(auth):
    req = Request("GET", "https://foo.com/bar")
    prepped = req.prepare()

    auth(prepped)

    assert "Authorization" in prepped.headers


def test_auth_token_call(auth):
    req = Request("GET", "https://foo.com/bar/api_clients")
    prepped = req.prepare()

    auth(prepped)

    assert "Authorization" not in prepped.headers
