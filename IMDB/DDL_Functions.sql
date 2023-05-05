/**//**//**//**//**/ -- FUNCTIONS -- /**//**//**//**//**/

CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS
    $set_timestamp$
        BEGIN
        NEW.last_updated = NOW();
        RETURN NEW;
        END;
    $set_timestamp$
LANGUAGE plpgsql;






/**//**//**//**//**/ -- TRIGGERS -- /**//**//**//**//**/

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON US_Congress
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();
