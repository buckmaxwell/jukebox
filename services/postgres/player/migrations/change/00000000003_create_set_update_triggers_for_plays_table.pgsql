CREATE TRIGGER set_plays_updated_at
  BEFORE UPDATE ON player.plays
  FOR EACH ROW
  EXECUTE PROCEDURE trigger_set_updated_at ();

