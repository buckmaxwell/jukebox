CREATE FUNCTION trigger_set_updated_at()
  RETURNS TRIGGER AS $$
  BEGIN
    NEW.updated_at = current_timestamp;
    RETURN NEW;
  END;
  $$ LANGUAGE plpgsql;