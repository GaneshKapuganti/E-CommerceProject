"""add category unique constraint and status enums

Revision ID: e755d4f567b1
Revises: 5130c5000fd2
Create Date: 2026-09-29 13:03:34.663457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'e755d4f567b1'
down_revision: Union[str, Sequence[str], None] = '5130c5000fd2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

order_status_enum = postgresql.ENUM(
    'pending', 'paid', 'shipped', 'delivered', 'cancelled', name='order_status'
)
payment_status_enum = postgresql.ENUM(
    'pending', 'completed', 'failed', 'refunded', name='payment_status'
)


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()

    # Normalize legacy free-text status values to the new enum's members
    # before locking the column down, so the type change below doesn't fail.
    op.execute("UPDATE orders SET status = 'paid' WHERE status = 'Order Confirmed'")
    op.execute("UPDATE payments SET status = 'completed' WHERE status = 'successful'")

    order_status_enum.create(bind, checkfirst=True)
    payment_status_enum.create(bind, checkfirst=True)

    op.create_unique_constraint('uq_categories_name', 'categories', ['name'])

    op.alter_column(
        'orders', 'status',
        existing_type=sa.VARCHAR(length=20),
        type_=order_status_enum,
        postgresql_using='status::order_status',
        existing_nullable=False,
    )
    op.alter_column(
        'payments', 'status',
        existing_type=sa.VARCHAR(length=20),
        type_=payment_status_enum,
        postgresql_using='status::payment_status',
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'payments', 'status',
        existing_type=payment_status_enum,
        type_=sa.VARCHAR(length=20),
        existing_nullable=False,
    )
    op.alter_column(
        'orders', 'status',
        existing_type=order_status_enum,
        type_=sa.VARCHAR(length=20),
        existing_nullable=False,
    )

    op.drop_constraint('uq_categories_name', 'categories', type_='unique')

    bind = op.get_bind()
    payment_status_enum.drop(bind, checkfirst=True)
    order_status_enum.drop(bind, checkfirst=True)
