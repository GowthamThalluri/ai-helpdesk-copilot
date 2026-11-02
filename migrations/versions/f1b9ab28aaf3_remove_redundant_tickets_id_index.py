"""remove redundant tickets id index"""

from alembic import op

revision = "f1b9ab28aaf3"
down_revision = "e91d904ff8b7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_index("ix_tickets_id", table_name="tickets")


def downgrade() -> None:
    op.create_index(
        "ix_tickets_id",
        "tickets",
        ["id"],
        unique=False,
    )