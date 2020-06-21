from requests.exceptions import HTTPError
from services.typeahead.app import app, redis
from services.typeahead.app import spotify_request
from unittest import TestCase
from unittest.mock import patch
import pytest
import services


# /tracks/
@patch.dict(
    "os.environ",
    {"SPOTIFY_REDIRECT_URI": "", "SPOTIFY_CLIENT_ID": "", "SPOTIFY_CLIENT_SECRET": ""},
)
@patch.object(spotify_request, "get")
@patch.object(redis.Redis, "get")
@patch.object(redis.Redis, "set")
class TestTracksRoute(TestCase):
    def test_get_tracks_happy_path_no_cache(
        self, redis_set, redis_get, spotify_request_get
    ):
        redis_get.return_value = None
        with app.test_client() as c:
            resp = c.get("/tracks/?service=spotify&q=Lollipop")
            redis_get.assert_called_with("spotify_Lollipop_track")
            spotify_request_get.assert_called()
            redis_set.assert_called()

            assert resp.json == []
            assert resp.status_code == 200

    def test_get_tracks_happy_path_cached(
        self, redis_set, redis_get, spotify_request_get
    ):
        redis_get.return_value = '[{"test":"test"}]'
        with app.test_client() as c:
            resp = c.get("/tracks/?service=spotify&q=Lollipop")
            redis_get.assert_called_with("spotify_Lollipop_track")
            spotify_request_get.assert_not_called()

            assert resp.json == [{"test": "test"}]
            assert resp.status_code == 200

    def test_get_tracks_not_authenticated(
        self, redis_set, redis_get, spotify_request_get
    ):
        def raise_(ex):
            raise ex

        redis_get.return_value = None
        spotify_request_get.return_value = type(
            "obj",
            (object,),
            {
                "status_code": 401,
                "raise_for_status": lambda: raise_(HTTPError("unauthenticated")),
            },
        )
        with app.test_client() as c:
            resp = c.get("/tracks/?service=spotify&q=Lollipop")
            redis_get.assert_called_with("spotify_Lollipop_track")
            spotify_request_get.assert_called()

            assert resp.json == {"error": "unauthenticated"}
            assert resp.status_code == 400

    def test_get_tracks_bad_service(self, redis_set, redis_get, spotify_request_get):

        with app.test_client() as c:
            resp = c.get("/tracks/?service=fakeserv&q=Lollipop")

            assert "fakeserv" in resp.json["error"]
            assert resp.status_code == 400

    def test_get_tracks_no_service(self, redis_set, redis_get, spotify_request_get):

        with app.test_client() as c:
            resp = c.get("/tracks/?q=Lollipop")

            assert resp.status_code == 400

    def test_get_tracks_no_query(self, redis_set, redis_get, spotify_request_get):

        with app.test_client() as c:
            resp = c.get("/tracks/?service=spotify")

            assert resp.status_code == 400

    def test_get_tracks_empty_query(self, redis_set, redis_get, spotify_request_get):

        redis_get.return_value = None
        with app.test_client() as c:
            resp = c.get("/tracks/?service=spotify&q=")

            assert resp.json == []
            assert resp.status_code == 200
