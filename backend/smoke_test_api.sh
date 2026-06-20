#!/usr/bin/env bash

set -euo pipefail

if [[ -z "${BACKEND_URL:-}" ]]; then
  echo "Debes definir BACKEND_URL, por ejemplo: BACKEND_URL=https://tu-backend.fastapicloud.dev ./smoke_test_api.sh"
  exit 1
fi

if ! command -v curl >/dev/null 2>&1; then
  echo "curl no esta instalado en el entorno actual."
  exit 1
fi

if ! command -v sed >/dev/null 2>&1; then
  echo "sed no esta instalado en el entorno actual."
  exit 1
fi

BASE_URL="${BACKEND_URL%/}"
TEACHER_EMAIL="teacher-fastapi@example.com"
TEACHER_PASSWORD="teacher-pass-123"
STUDENT_EMAIL="student-fastapi@example.com"
STUDENT_PASSWORD="student-pass-123"

echo "[1/5] Verificando health endpoint"
curl --fail --silent "$BASE_URL/api/health"
echo

echo "[2/5] Registrando profesor"
curl --fail --silent -X POST "$BASE_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$TEACHER_EMAIL\",\"password\":\"$TEACHER_PASSWORD\",\"full_name\":\"Teacher FastAPI\",\"roles\":[\"teacher\"]}" \
  || true
echo

echo "[3/5] Registrando estudiante"
curl --fail --silent -X POST "$BASE_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$STUDENT_EMAIL\",\"password\":\"$STUDENT_PASSWORD\",\"full_name\":\"Student FastAPI\",\"roles\":[\"student\"]}" \
  || true
echo

echo "[4/5] Iniciando sesion de profesor"
teacher_login_response="$(curl --fail --silent -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$TEACHER_EMAIL\",\"password\":\"$TEACHER_PASSWORD\"}")"
echo "$teacher_login_response"

teacher_token="$(printf '%s' "$teacher_login_response" | sed -n 's/.*"token"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"

if [[ -z "$teacher_token" ]]; then
  echo "No se pudo extraer el token del profesor desde la respuesta de login."
  exit 1
fi

echo "[5/5] Creando seccion academica"
curl --fail --silent -X POST "$BASE_URL/api/academic/sections" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $teacher_token" \
  -d '{"course_code":"PN-201","course_name":"Programacion Numerica II","term_name":"2026-II","term_starts_on":"2026-07-01","term_ends_on":"2026-12-01","section_name":"B"}'
echo

echo "Smoke test completado correctamente."