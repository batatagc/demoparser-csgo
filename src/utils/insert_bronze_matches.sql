INSERT INTO bronze_matches 
VALUES (
    {match_id}, 
    '{description}',
    NULL, 
    '{created_at}', 
    '{created_at}'
) 
ON CONFLICT DO NOTHING;