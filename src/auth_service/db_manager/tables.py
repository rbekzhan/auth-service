import uuid
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy import MetaData, UUID

metadata = MetaData()

VerifyCode = sa.Table(
    "verify_code", metadata,
    sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True),
    sa.Column("phone_number", sa.String, nullable=False),
    sa.Column("code", sa.String, nullable=False),
    sa.Column("confirmed_client_code", sa.String(4), nullable=True),
    sa.Column("confirm_code", sa.Boolean, nullable=False),
    sa.Column("attempt_count", sa.Integer, nullable=False),
    sa.Column("created_at", sa.DateTime, default=datetime.utcnow),
    sa.Column("updated_at", sa.DateTime, onupdate=datetime.utcnow)
)

UserTable = sa.Table(
    "users", metadata,
    sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True),
    sa.Column("phone_number", sa.String, nullable=False, unique=True),
    sa.Column("email", sa.String, nullable=True),
    sa.Column("created_at", sa.DateTime, default=datetime.utcnow),
    sa.Column("updated_at", sa.DateTime, onupdate=datetime.utcnow),
)

AccountTable = sa.Table(
    "accounts", metadata,
    sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True),
    sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id")),
    sa.Column("username", sa.String, nullable=False, unique=True),
    sa.Column("first_name", sa.String, nullable=True),
    sa.Column("last_name", sa.String, nullable=True),
    sa.Column("bio", sa.String, nullable=True),
    sa.Column("avatar_path", sa.String, nullable=True),
    sa.Column("created_at", sa.DateTime, default=datetime.utcnow),
    sa.Column("updated_at", sa.DateTime, onupdate=datetime.utcnow)
)

ContactTable = sa.Table(
    "contacts", metadata,
    sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True),
    sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id")),
    sa.Column("phone_number", sa.String, nullable=True, unique=True),
    sa.Column("first_name", sa.String, nullable=True),
    sa.Column("last_name", sa.String, nullable=True),
    sa.Column("created_at", sa.DateTime, default=datetime.utcnow),
    sa.Column("updated_at", sa.DateTime, onupdate=datetime.utcnow),
    sa.UniqueConstraint("user_id", "phone_number", name="user_phone_number_x")
)

