from services.room_settings.app import (
    app,
    async_messenger,
    login_required,
    r,
    random,
    redis,
    uuid,
    redis_wait,
    spotify_login,
)
from unittest.mock import MagicMock, patch
from unittest import TestCase
import pytest
import services


def generator_from_list(lst):
    for el in lst:
        yield el


# Routes

## /host
@patch.dict(
    "os.environ",
    {"SPOTIFY_REDIRECT_URI": "", "SPOTIFY_CLIENT_ID": "", "SPOTIFY_CLIENT_SECRET": ""},
)
@patch.object(random, "choice", return_value="A")
@patch.object(redis.Redis, "set")
@patch.object(redis.Redis, "get")
@patch.object(async_messenger, "send")
@patch.object(services.room_settings.redis_wait, "redis_wait")
class TestHostRoute(TestCase):
    def test_get_host(self, redis_wait, am_send, redis_get, redis_set, rand_choice):
        with app.test_client() as c:
            c.set_cookie("localhost", "ROOM_SETTINGS", "xxx")
            resp = c.get("/host/")
            assert resp.status_code == 200

    def test_get_host_no_room_code_cookie(
        self, redis_wait, am_send, redis_get, redis_set, rand_choice
    ):

        gen = generator_from_list([1, 1, None, 1])

        def authorization_found_but_no_corresponding_room_code(*args):
            return next(gen)

        redis_get.side_effect = authorization_found_but_no_corresponding_room_code
        with app.test_client() as c:
            c.set_cookie("localhost", "SERVICE", "spotify")
            c.set_cookie("localhost", "ROOM_SETTINGS", "xxx")
            resp = c.get("/host/")
            redis_set.assert_any_call("xxx_room_code", "AAAAA")
            redis_set.assert_any_call("AAAAA", 1, ex=60 * 60 * 24)
            redis_set.assert_any_call("AAAAA_service", "spotify", ex=60 * 60 * 24)

            assert "AAAAA" in str(resp.data)
            assert resp.status_code == 200

    def test_get_host_not_authorized_service_given(
        self, redis_wait, am_send, redis_get, redis_set, rand_choice
    ):
        gen = generator_from_list([None])

        def no_authorization_found(*args):
            return next(gen)

        redis_get.side_effect = no_authorization_found
        with app.test_client() as c:
            c.set_cookie("localhost", "SERVICE", "spotify")
            resp = c.get("/host/")
            assert "/host/spotify-login" in resp.headers["Location"]
            assert resp.status_code == 302

    def test_get_host_not_authorized_no_service(
        self, redis_wait, am_send, redis_get, redis_set, rand_choice
    ):
        gen = generator_from_list([None])

        def no_authorization_found(*args):
            return next(gen)

        redis_get.side_effect = no_authorization_found
        with app.test_client() as c:
            resp = c.get("/host/")
            assert "/host/service-select" in resp.headers["Location"]
            assert resp.status_code == 302

    def test_get_host_not_authorized_bad_service(
        self, redis_wait, am_send, redis_get, redis_set, rand_choice
    ):
        gen = generator_from_list([None])

        def no_authorization_found(*args):
            return next(gen)

        redis_get.side_effect = no_authorization_found
        with app.test_client() as c:
            c.set_cookie("localhost", "SERVICE", "not_a_service")
            resp = c.get("/host/")
            assert "/host/service-select" in resp.headers["Location"]
            assert resp.status_code == 302


## /host/room/<room_code>
@patch.dict(
    "os.environ",
    {"SPOTIFY_REDIRECT_URI": "", "SPOTIFY_CLIENT_ID": "", "SPOTIFY_CLIENT_SECRET": ""},
)
@patch.object(redis.Redis, "get")
class TestPublicRoomRoute(TestCase):
    def test_get_public_room_with_valid_room_code(self, redis_get):
        gen = generator_from_list([1, "spotify", "spotify"])

        def room_code_has_authorization_and_service(*args):
            return next(gen)

        redis_get.side_effect = room_code_has_authorization_and_service
        with app.test_client() as c:
            resp = c.get("/host/room/ABCXY")
            assert resp.status_code == 200
            assert resp.json == {"room_code": "ABCXY", "service": "spotify"}

    def test_get_public_room_with_invalid_room_code(self, redis_get):
        gen = generator_from_list([None, "spotify", "spotify"])

        def room_code_has_authorization_and_service(*args):
            return next(gen)

        redis_get.side_effect = room_code_has_authorization_and_service
        with app.test_client() as c:
            resp = c.get("/host/room/ABCXY")
            assert resp.status_code == 404
            assert resp.json == {"error": "resource not found"}

    def test_get_public_room_with_valid_room_code_but_for_some_reason_service_is_missing(
        self, redis_get
    ):
        gen = generator_from_list([1, None, None])

        def room_code_has_authorization_and_service(*args):
            return next(gen)

        redis_get.side_effect = room_code_has_authorization_and_service
        with app.test_client() as c:
            resp = c.get("/host/room/ABCXY")
            assert resp.status_code == 404
            assert resp.json == {"error": "resource not found"}

    def test_post_public_room(self, redis_get):
        with app.test_client() as c:
            resp = c.post("/host/room/ABCXY")
            assert resp.status_code == 405


## /host/spotify-login

# TODO: defferring for now because of testing difficulties

## /host/service-select
def test_get_service_select():
    with app.test_client() as c:
        resp = c.get("/host/service-select")
        assert resp.status_code == 200
        assert "/host/spotify-login" in str(resp.data)


## /host/spotify
## /host
# @patch.object(services.room_settings.redis_wait, "redis_wait", return_value=1)
@patch.dict(
    "os.environ",
    {"SPOTIFY_REDIRECT_URI": "", "SPOTIFY_CLIENT_ID": "", "SPOTIFY_CLIENT_SECRET": ""},
)
@patch.object(uuid, "uuid4", return_value="xxx")
@patch.object(redis.Redis, "get")
@patch.object(async_messenger, "send")
class TestSpotifyRoute(TestCase):
    def test_get_spotify_happy_path(self, am_send, redis_get, uuid4):
        gen = generator_from_list(["true", 1])

        def state_exists(*args):
            return next(gen)

        redis_get.side_effect = state_exists
        with app.test_client() as c:
            resp = c.get(f"/host/spotify?code=thecode&state=thestate")
            am_send.assert_any_call(
                "authorizer.create_authorization",
                {"code": "thecode", "key": "xxx", "service": "spotify"},
            )
            am_send.assert_any_call(
                "authorizer.make_authorized_request",
                {
                    "http_verb": "get",
                    "url": "https://api.spotify.com/v1/me",
                    "authorization_id": 1,
                    "queue": "user.find_or_create_user",
                },
            )
            assert "/host/" in resp.headers["Location"]
            assert "ROOM_SETTINGS=xxx" in str(resp.headers)
            assert "SERVICE=spotify" in str(resp.headers)
            assert resp.status_code == 302

    def test_get_spotify_bad_state(self, am_send, redis_get, uuid4):
        gen = generator_from_list([None])

        def state_exists(*args):
            return next(gen)

        redis_get.side_effect = state_exists
        with app.test_client() as c:
            resp = c.get(f"/host/spotify?code=thecode&state=thestate")
            am_send.assert_not_called()
            assert "you are not logged in" in resp.json["error"]
            assert resp.status_code == 400

    def test_get_spotify_no_code(self, am_send, redis_get, uuid4):
        gen = generator_from_list(["true", 1])

        def state_exists(*args):
            return next(gen)

        redis_get.side_effect = state_exists
        with app.test_client() as c:
            resp = c.get(f"/host/spotify?state=thestate")
            am_send.assert_not_called()
            assert "you are not logged in" in resp.json["error"]
            assert resp.status_code == 400
