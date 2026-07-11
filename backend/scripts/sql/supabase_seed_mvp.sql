-- Seed minimo e idempotente para el MVP academico en Supabase/PostgreSQL.
-- Ejecutar despues de alembic upgrade head.

BEGIN;

INSERT INTO roles (name, description)
SELECT 'student', 'Rol estudiante'
WHERE NOT EXISTS (SELECT 1 FROM roles WHERE name = 'student');

INSERT INTO roles (name, description)
SELECT 'teacher', 'Rol profesor'
WHERE NOT EXISTS (SELECT 1 FROM roles WHERE name = 'teacher');

INSERT INTO roles (name, description)
SELECT 'admin', 'Rol administrador'
WHERE NOT EXISTS (SELECT 1 FROM roles WHERE name = 'admin');

INSERT INTO topics (name, area)
SELECT 'Raices', 'Metodos numericos'
WHERE NOT EXISTS (SELECT 1 FROM topics WHERE name = 'Raices');

INSERT INTO learning_units (topic_id, title, description)
SELECT t.id, 'Metodos de raices', 'Unidad base para actividades de biseccion, Newton, secante y punto fijo.'
FROM topics t
WHERE t.name = 'Raices'
  AND NOT EXISTS (
    SELECT 1
    FROM learning_units lu
    WHERE lu.topic_id = t.id
      AND lu.title = 'Metodos de raices'
  );

COMMIT;
