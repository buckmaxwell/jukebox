# Async Messenger

Queue messages to a rabbitmq server. Requires a running rabbitmq server to work.

```python
async_messenger.send('name_of_queue', {'msg':'test'})
```
