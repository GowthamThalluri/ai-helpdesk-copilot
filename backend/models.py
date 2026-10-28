from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(120), nullable=False)

    description: Mapped[str] = mapped_column(Text, nullable=False)

    category: Mapped[str] = mapped_column(String(60), nullable=False)

    priority: Mapped[str] = mapped_column(String(20), nullable=False)

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="Open",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )