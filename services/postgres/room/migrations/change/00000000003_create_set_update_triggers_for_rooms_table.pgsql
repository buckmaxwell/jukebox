CREATE TRIGGER set_rooms_updated_at
  BEFORE UPDATE ON room.rooms
  FOR EACH ROW
  EXECUTE PROCEDURE trigger_set_updated_at ();

