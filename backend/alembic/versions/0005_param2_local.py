"""Add BharatGen Param2 to the Local (free) provider, for installs that already ran 0004.

Data only and idempotent; skips an install without the provider.

Revision ID: 0005_param2_local
Revises: 0004_sarvam_and_local
"""

from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0005_param2_local"
down_revision: Union[str, Sequence[str], None] = "0004_sarvam_and_local"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

MODEL = ("param2-17b", "BharatGen Param2 17B (free, on this server)",
         "Indian open-weight model, 22 Indian languages, the fastest free model here. Non-commercial use only", 32000)


def upgrade() -> None:
    conn = op.get_bind()
    meta = sa.MetaData()
    api_provider = sa.Table("api_provider", meta, autoload_with=conn)
    ai_model = sa.Table("ai_model", meta, autoload_with=conn)
    provider_id = conn.execute(sa.select(api_provider.c.id).where(api_provider.c.name == "Local (free)")).scalar()
    if provider_id is None:
        return
    name, display, description, context = MODEL
    if conn.execute(sa.select(ai_model.c.id).where(ai_model.c.provider_id == provider_id,
                                                   ai_model.c.name == name)).first():
        return
    lowest = conn.execute(sa.select(sa.func.min(ai_model.c.sort_order))
                          .where(ai_model.c.provider_id == provider_id)).scalar() or 1
    conn.execute(ai_model.insert().values(
        name=name, display_name=display, description=description, provider_id=provider_id,
        context_window=context, is_latest=True, sort_order=lowest - 1, is_active=True,
        created_at=datetime.utcnow()))


def downgrade() -> None:
    """Not used: going back means restoring the backup taken before the upgrade."""
