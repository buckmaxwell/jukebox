import os

SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
SPOTIFY_REDIRECT_URI = os.environ["SPOTIFY_REDIRECT_URI"]

SPOTIFY_API_SCOPES = [
    "playlist-modify-private",
    "user-modify-playback-state",
    "user-read-currently-playing",
    "user-read-playback-state",
    "streaming",
    "app-remote-control",
    "playlist-modify-public",
    "playlist-read-collaborative",
    "playlist-read-private",
    "user-library-modify",
    "user-library-read",
    "user-read-email",
    "user-read-recently-played",
    "user-top-read",
]
