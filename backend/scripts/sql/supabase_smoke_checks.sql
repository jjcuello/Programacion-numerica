-- Consultas de verificacion rapida para confirmar que el esquema MVP
-- esta desplegado y listo para el flujo web de profesor/estudiante.

SELECT tablename
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename IN (
    'users',
    'roles',
    'user_roles',
    'profiles',
    'academic_terms',
    'courses',
    'course_sections',
    'enrollments',
    'topics',
    'learning_units',
    'activities',
    'activity_versions',
    'assignments',
    'submissions',
    'attempts',
    'feedback'
  )
ORDER BY tablename;

SELECT name, description
FROM roles
ORDER BY name;

SELECT t.name AS topic_name, lu.title AS learning_unit
FROM topics t
LEFT JOIN learning_units lu ON lu.topic_id = t.id
WHERE t.name = 'Raices'
ORDER BY lu.title;

SELECT
  (SELECT COUNT(*) FROM users) AS users_count,
  (SELECT COUNT(*) FROM course_sections) AS sections_count,
  (SELECT COUNT(*) FROM assignments) AS assignments_count,
  (SELECT COUNT(*) FROM attempts) AS attempts_count;
