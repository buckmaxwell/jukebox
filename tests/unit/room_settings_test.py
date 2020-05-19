
from services.room_settings.app import app, redis, async_messenger
from unittest.mock import MagicMock, patch
import pytest
import services
import os

# Routes


## /host
@patch.dict(
    "os.environ",
    {"SPOTIFY_REDIRECT_URI": "", "SPOTIFY_CLIENT_ID": "", "SPOTIFY_CLIENT_SECRET": ""},
)
@patch.object(redis.Redis, "set")
@patch.object(redis.Redis, "get")
@patch.object(async_messenger, "send")
@patch.object(services.room_settings.redis_wait, "redis_wait")
def test_get_host(redis_wait, am_send, redis_get, redis_set):
    with app.test_client() as c:
        c.set_cookie("localhost", "ROOM_SETTINGS", "xxx")
        c.set_cookie("localhost", "SERVICE", "spotify")
        resp = c.get("/host/")
        assert resp.status_code == 200


# no auth id, service cookie is spotify, service select


## /host/room/<room_code>

## /host/encore

## /host/service-select

## /host/spotify-login

## /host/spotify


# Other methods

# login required
