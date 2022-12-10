SELECT * FROM teams;
DO $$
DECLARE
    team CHAR(25);
	id INT;
BEGIN
	id := 10;
    team := 'team';
    FOR counter IN 1..10
        LOOP
		   INSERT INTO teams(team_id, team_name) 
		   VALUES (id + counter, team || counter);
        END LOOP;
END;
$$






