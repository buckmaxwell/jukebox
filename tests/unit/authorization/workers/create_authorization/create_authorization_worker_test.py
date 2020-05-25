from unittest.mock import patch
from unittest import TestCase
import pytest


@patch.object(redis.Redis, "get")
@patch.object(async_messenger, "send")
@patch.object(services.player.app, "spotify_play_song")
class TestPlayer(TestCase):
    def test_post_song_happy_path(self, play_song, am_send, redis_get):