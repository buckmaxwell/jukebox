CREATE TABLE player.plays (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
  isrc varchar,
  upc varchar,
  ean varchar,
  spotify_id varchar,
  room_code varchar,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
  deleted_at timestamp
);

