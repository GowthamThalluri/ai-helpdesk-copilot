"""create tickets table

Revision ID: e91d904ff8b7
Revises:
"""

from alembic import op
import sqlalchemy as sa

revision = "e91d904ff8b7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tickets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=60), nullable=False),
        sa.Column("priority", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Preserve the historical index. Revision 2 will remove it.
    op.create_index(
        "ix_tickets_id",
        "tickets",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_tickets_id", table_name="tickets")
    op.drop_table("tickets")