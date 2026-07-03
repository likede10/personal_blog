from datetime import datetime
from enum import Enum

from sqlalchemy import BigInteger, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class UserRole(str, Enum):
    ADMIN = "admin"
    AUTHOR = "author"
    USER = "user"


class UserStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    PENDING = "pending"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="用户ID",
    )

    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
        comment="用户名，用于登录或展示",
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
        comment="邮箱，用于登录/找回密码",
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="加密后的密码，不能存明文密码",
    )

    nickname: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True,
        comment="展示昵称",
        default="阳光开朗的鸟",
    )

    avatar_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="头像地址",
    )

    bio: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="个人简介",
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=UserRole.USER.value,
        index=True,
        comment="角色：admin/author/user",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=UserStatus.ACTIVE.value,
        index=True,
        comment="状态：active/disabled/pending",
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="最后登录时间",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        comment="创建时间",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间",
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        index=True,
        comment="软删除时间",
    )