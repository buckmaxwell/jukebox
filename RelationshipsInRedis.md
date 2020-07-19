
# Redis Relationships

Redis allows services to communicate with each other. Here is a map of the
data relationships in redis.

- room_code: [user_id, user_id, ...]

GET room_code returns a list of the users in the room, including the owner and any followers.

- user_id: auth_id

GET user_id will return the active authorization for the user if there is one.

- auth_id: service

GET auth_id will return the service the authorization corresponds with.



