from services.room_settings.app import (
    app,
    redis,
    async_messenger,
    random,
    login_required,
    r,
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


## /host/encore

## /host/service-select

## /host/spotify-login

## /host/spotify


# Other methods

# login required
