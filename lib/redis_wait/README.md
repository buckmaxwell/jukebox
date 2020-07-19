# Redis wait 

Wait on a redis key to exist.


```python
from redis_wait import redis_wait
import redis

r = redis.Redis()
redis_wait(r, 'some_key')
```
