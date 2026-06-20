from __future__ import annotations

import base64
import hashlib
import hmac
import os
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from src.infrastructure.storage.sql_models import ProfileModel, RoleModel, UserModel, UserRoleModel
from src.infrastructure.storage.sql_repositories import SqlAlchemyUserRepository


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _b64url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode((value + padding).encode("ascii"))


@dataclass(frozen=True)
class AuthenticatedUser:
    user_id: str
    email: str
    roles: tuple[str, ...]


class PasswordHasher:
    iterations = 390000

    def hash_password(self, password: str) -> str:
        salt = secrets.token_bytes(16)
        derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, self.iterations)
        return f"pbkdf2_sha256${self.iterations}${_b64url_encode(salt)}${_b64url_encode(derived)}"

    def verify_password(self, password: str, encoded_hash: str) -> bool:
        try:
            algorithm, iterations, salt_b64, digest_b64 = encoded_hash.split("$", 3)
        except ValueError:
            return False
        if algorithm != "pbkdf2_sha256":
            return False
        salt = _b64url_decode(salt_b64)
        expected = _b64url_decode(digest_b64)
        candidate = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, int(iterations))
        return hmac.compare_digest(candidate, expected)


class TokenService:
    def __init__(self, secret: str, expires_in_hours: int = 12, algorithm: str = "HS256"):
        self.secret = secret
        self.expires_in_hours = expires_in_hours
        self.algorithm = algorithm

    def issue(self, user: UserModel, roles: tuple[str, ...]) -> str:
        payload = {
            "sub": user.id,
            "email": user.email,
            "roles": list(roles),
            "exp": _utcnow() + timedelta(hours=self.expires_in_hours),
            "iat": _utcnow(),
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def verify(self, token: str) -> AuthenticatedUser:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError as error:
            raise ValueError("Token expirado.") from error
        except jwt.InvalidTokenError as error:
            raise ValueError("Token invalido.") from error

        return AuthenticatedUser(
            user_id=str(payload["sub"]),
            email=str(payload["email"]),
            roles=tuple(str(role) for role in payload.get("roles", [])),
        )


class AuthService:
    def __init__(self, session_factory: sessionmaker[Session], token_service: TokenService | None = None):
        self.session_factory = session_factory
        self.password_hasher = PasswordHasher()
        self.token_service = token_service or TokenService(os.getenv("AUTH_TOKEN_SECRET", "dev-secret-change-me"))

    def register_user(
        self,
        *,
        email: str,
        password: str,
        full_name: str,
        role_names: tuple[str, ...] = ("student",),
        institutional_code: str | None = None,
    ) -> dict[str, object]:
        normalized_email = email.strip().lower()
        if not normalized_email or "@" not in normalized_email:
            raise ValueError("Correo invalido.")
        if len(password) < 8:
            raise ValueError("La contrasena debe tener al menos 8 caracteres.")
        if not full_name.strip():
            raise ValueError("El nombre completo es obligatorio.")

        with self.session_factory() as session:
            user_repository = SqlAlchemyUserRepository(session)
            existing = user_repository.get_by_email(normalized_email)
            if existing is not None:
                raise ValueError("Ya existe un usuario con ese correo.")

            user = user_repository.create(
                email=normalized_email,
                password_hash=self.password_hasher.hash_password(password),
                status="active",
            )
            session.add(
                ProfileModel(
                    user_id=user.id,
                    full_name=full_name.strip(),
                    institutional_code=institutional_code,
                )
            )
            role_models = self._resolve_roles(session, role_names)
            for role in role_models:
                session.add(UserRoleModel(user_id=user.id, role_id=role.id))
            session.commit()

            roles = tuple(role.name for role in role_models)
            token = self.token_service.issue(user, roles)
            return {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": full_name.strip(),
                    "roles": list(roles),
                },
                "token": token,
            }

    def login(self, *, email: str, password: str) -> dict[str, object]:
        normalized_email = email.strip().lower()
        with self.session_factory() as session:
            user_repository = SqlAlchemyUserRepository(session)
            user = user_repository.get_by_email(normalized_email)
            if user is None or not self.password_hasher.verify_password(password, user.password_hash):
                raise ValueError("Credenciales invalidas.")
            roles = self._get_role_names(session, user.id)
            token = self.token_service.issue(user, roles)
            profile = session.get(ProfileModel, user.id)
            return {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": profile.full_name if profile is not None else user.email,
                    "roles": list(roles),
                },
                "token": token,
            }

    def authenticate(self, token: str) -> AuthenticatedUser:
        return self.token_service.verify(token)

    def _resolve_roles(self, session: Session, role_names: tuple[str, ...]) -> list[RoleModel]:
        normalized_role_names = tuple(sorted({role.strip().lower() for role in role_names if role.strip()}))
        if not normalized_role_names:
            normalized_role_names = ("student",)
        statement = select(RoleModel).where(RoleModel.name.in_(normalized_role_names))
        existing_roles = {role.name: role for role in session.execute(statement).scalars()}
        role_models = []
        for role_name in normalized_role_names:
            role = existing_roles.get(role_name)
            if role is None:
                role = RoleModel(name=role_name, description=f"Rol {role_name}")
                session.add(role)
                session.flush()
            role_models.append(role)
        return role_models

    def _get_role_names(self, session: Session, user_id: str) -> tuple[str, ...]:
        statement = (
            select(RoleModel.name)
            .join(UserRoleModel, UserRoleModel.role_id == RoleModel.id)
            .where(UserRoleModel.user_id == user_id)
            .order_by(RoleModel.name)
        )
        return tuple(session.execute(statement).scalars())
