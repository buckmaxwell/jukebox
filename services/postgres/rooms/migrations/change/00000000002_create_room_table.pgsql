CREATE TABLE room.rooms (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
  code varchar,
  host integer,
  expiration timestamp,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
  deleted_at timestamp
);

