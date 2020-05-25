from services.player.app import app, redis, async_messenger
from services.player.app import spotify_play_song, uuid
from unittest.mock import MagicMock, patch
from unittest import TestCase
import pytest
import services


@patch.object(redis.Redis, "get")
@patch.object(async_messenger, "send")
@patch.object(services.player.app, "spotify_play_song")
class TestPlayer(TestCase):
    def test_post_song_happy_path(self, play_song, am_send, redis_get):
        with app.test_client() as c:
            resp = c.post(
                "/player/", json={"room_code": "", "service": "spotify", "uri": ""}
            )
            assert resp.status_code == 204
            play_song.assert_called()

    def test_post_song_bad_service(self, play_song, am_send, redis_get):
        with app.test_client() as c:
            resp = c.post(
                "/player/", json={"room_code": "", "service": "jupiter", "uri": ""}
            )
            assert resp.status_code == 400
            assert (
                resp.get_json()["error"]
                == "AttributeError:module 'services.player.app' has no attribute 'jupiter_play_song'"
            )

    def test_post_song_body_not_json(self, play_song, am_send, redis_get):
        with app.test_client() as c:
            resp = c.post(
                "/player/", data={"room_code": "", "service": "jupiter", "uri": ""}
            )
            assert resp.status_code == 400
            assert resp.get_json()["error"] == "PlayerError:request must be json"

    def test_post_bad_room_code(self, play_song, am_send, redis_get):
        redis_get.return_value = None
        with app.test_client() as c:
            resp = c.post(
                "/player/", json={"room_code": "", "service": "spotify", "uri": ""}
            )
            assert resp.status_code == 404
            assert resp.get_json()["error"] == "room not found"

    def test_post_no_service(self, play_song, am_send, redis_get):
        with app.test_client() as c:
            resp = c.post("/player/", json={"uri": "", "room_code": ""})
            assert resp.status_code == 400
            assert resp.get_json()["error"] == "KeyError:'service'"

    def test_post_no_room_code(self, play_song, am_send, redis_get):
        with app.test_client() as c:
            resp = c.post("/player/", json={"service": "spotify", "uri": ""})
            assert resp.status_code == 400
            assert resp.get_json()["error"] == "KeyError:'room_code'"

    def test_post_no_uri(self, play_song, am_send, redis_get):
        play_song.side_effect = KeyError("uri")
        with app.test_client() as c:
            resp = c.post("/player/", json={"room_code": "", "service": "spotify"})
            assert resp.status_code == 400
            assert resp.get_json()["error"] == "KeyError:'uri'"

    def test_called_with_get(self, play_song, am_send, redis_get):
        with app.test_client() as c:
            resp = c.get("/player/")
            assert resp.status_code == 405


@patch.object(redis.Redis, "get")
@patch.object(async_messenger, "send")
@patch.object(uuid, "uuid4", return_value="xxx")
class TestSpotifyPlaySong(TestCase):
    def test_spotify_play_song_happy_path(self, uuid, am_send, redis_get):
        request = MagicMock()
        request.get_json.return_value = {"uri": "foo"}
        spotify_play_song(request, 1)
        am_send.assert_any_call(
            "authorizer.make_authorized_request",
            {
                "http_verb": "post",
                "url": f"https://api.spotify.com/v1/me/player/queue?uri=foo",
                "authorization_id": 1,
                "key": "xxx",
                "expires_in": 60 * 60,
            },
        )
        am_send.assert_any_call(
            "authorizer.make_authorized_request",
            {
                "http_verb": "put",
                "url": "https://api.spotify.com/v1/me/player/play",
                "authorization_id": 1,
                "key": "xxx",
                "expires_in": 60 * 60,
            },
        )

    def test_spotify_play_song_no_uri(self, uuid, am_send, redis_get):
        with pytest.raises(KeyError, match=r".*uri.*"):
            request = MagicMock()
            request.get_json.return_value = {}
            spotify_play_song(request, 1)
            am_send.assert_not_called()
