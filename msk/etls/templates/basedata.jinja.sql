SELECT DISTINCT ON (pj.patient_id, pj.journey_id)
    pj.patient_id, 
    pj.journey_id AS patient_journey_id,
    a.id AS activity_id, 
    a.content_slug AS activity_content_slug, 
    s.id AS schedule_id, 
    s.slug AS schedule_slug
FROM patient_journey pj
JOIN journey_activity ja ON pj.journey_id = ja.journey_id
JOIN activity a ON ja.activity_id = a.id
JOIN schedule s ON a.schedule_id = s.id
ORDER BY pj.patient_id, pj.journey_id
LIMIT {{ limit|int }} OFFSET {{ offset|int }};