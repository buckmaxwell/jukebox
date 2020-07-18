CREATE TABLE room.followers (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
  room_id uuid REFERENCES room.rooms (id),
  user_id uuid REFERENCES _user.users (id),
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
  deleted_at timestamp
);

