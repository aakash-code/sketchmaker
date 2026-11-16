"""Keep only the fast free model (Param2) on the Local (free) list.

GPT-OSS 20B and Sarvam-M answer at about one word a second on this server's two cores,
so a script ran past the ten-minute limit and failed. They are switched off (not
deleted), and a default, backup or user choice pointing at them is cleared, so the app
moves to a model that answers. Idempotent.

Revision ID: 0006_local_fast_only
Revises: 0005_param2_local
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0006_local_fast_only"
down_revision: Union[str, Sequence[str], None] = "0005_param2_local"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SLOW = ("gpt-oss:20b", "hf.co/bartowski/sarvamai_sarvam-m-GGUF:Q4_K_M")


def upgrade() -> None:
    conn = op.get_bind()
    meta = sa.MetaData()
    api_provider = sa.Table("api_provider", meta, autoload_with=conn)
    ai_model = sa.Table("ai_model", meta, autoload_with=conn)
    api_settings = sa.Table("api_settings", meta, autoload_with=conn)
    user = sa.Table("user", meta, autoload_with=conn)
    provider_id = conn.execute(sa.select(api_provider.c.id).where(api_provider.c.name == "Local (free)")).scalar()
    if provider_id is None:
        return
    ids = [r[0] for r in conn.execute(sa.select(ai_model.c.id).where(
        ai_model.c.provider_id == provider_id, ai_model.c.name.in_(SLOW)))]
    if not ids:
        return
    conn.execute(ai_model.update().where(ai_model.c.id.in_(ids)).values(is_active=False))
    conn.execute(user.update().where(user.c.selected_model_id.in_(ids)).values(selected_model_id=None))
    conn.execute(api_settings.update().where(api_settings.c.default_model_id.in_(ids))
                 .values(default_model_id=None, default_provider_id=None))
    conn.execute(api_settings.update().where(api_settings.c.fallback_model_id.in_(ids))
                 .values(fallback_model_id=None, fallback_provider_id=None))


def downgrade() -> None:
    """Not used: going back means restoring the backup taken before the upgrade."""
