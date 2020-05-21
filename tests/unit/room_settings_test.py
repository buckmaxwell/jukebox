
from services.room_settings.app import app, redis, async_messenger, random, login_required,r
from unittest.mock import MagicMock, patch
from unittest import TestCase
import pytest
import services

# Routes

## /host
@patch.dict(
    "os.environ",
    {"SPOTIFY_REDIRECT_URI": "", "SPOTIFY_CLIENT_ID": "", "SPOTIFY_CLIENT_SECRET": ""},
)
@patch.object(random, "choice", return_value='A')
@patch.object(redis.Redis, "set")
@patch.object(redis.Redis, "get")
@patch.object(async_messenger, "send")
@patch.object(services.room_settings.redis_wait, "redis_wait")
class TestHostRoute(TestCase):

    def test_get_host(self, redis_wait, am_send, redis_get, redis_set, rand_choice):
        with app.test_client() as c:
            c.set_cookie("localhost", "ROOM_SETTINGS", "xxx")
            c.set_cookie("localhost", "SERVICE", "spotify")
            resp = c.get("/host/")
            assert resp.status_code == 200

    def test_room_code_set_when_no_room_code(self, redis_wait, am_send, redis_get,redis_set, rand_choice):
        def generator_from_list(lst):
            for el in lst:
                yield el

        otn = generator_from_list([1,1, None,1])

        def one_then_none(*args):
            return next(otn)

        redis_get.side_effect = one_then_none
        with app.test_client() as c:
            c.set_cookie("localhost", "SERVICE", "spotify")
            c.set_cookie("localhost", "ROOM_SETTINGS", "xxx")
            resp = c.get("/host/")
            redis_set.assert_any_call("xxx_room_code", 'AAAAA')
            redis_set.assert_any_call("AAAAA", 1, ex=60 * 60 * 24)
            redis_set.assert_any_call("AAAAA_service", 'spotify', ex=60 * 60 * 24)

            assert 'AAAAA' in str(resp.data)
            assert resp.status_code == 200



# no auth id, service cookie is spotify, service select


## /host/room/<room_code>

## /host/encore

## /host/service-select

## /host/spotify-login

## /host/spotify


# Other methods

# login required
