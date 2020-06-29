CREATE TABLE room.rooms (
  id serial PRIMARY KEY,
  code varchar,
  host integer,
  expiration timestamp,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
  deleted_at timestamp
);

