# Synchronous Spotify Request 

*A wrapper around python requests that takes care of client credential*
*authorization for spotify*

Make syncronous client requests to spotifty. These request types don't have
the ability to access any user data.

```python
import spotify_request

spotify_request.get("some_spotify_url",header={'blah':'x'}, otherkwargs='blah' )
```
