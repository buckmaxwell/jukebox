# Synchronous Spotify Request 

Queue messages to a rabbitmq server. Requires a running rabbitmq server to work.

```python
from sync_spotify_request import user, client

params = {'headers':{'SOMEHEADER':1'}}
client.get("https://spotify.com/api",params )
user.get('http://spotify.com/api", params)
```
