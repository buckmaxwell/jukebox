CREATE TRIGGER set_followers_updated_at
  BEFORE UPDATE ON room.followers
  FOR EACH ROW
  EXECUTE PROCEDURE trigger_set_updated_at ();

