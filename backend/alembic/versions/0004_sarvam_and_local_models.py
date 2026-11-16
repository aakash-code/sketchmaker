"""Add the Sarvam and Local (free) language model providers and their models, for
existing installs. A new install gets them from seed_defaults.

Data only, and idempotent: a provider or model already there is left as it is, and
nothing the owner chose (default, fallback, their own models) is touched.

Revision ID: 0004_sarvam_and_local
Revises: 0003_faceless_studio
"""

from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0004_sarvam_and_local"
down_revision: Union[str, Sequence[str], None] = "0003_faceless_studio"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

PROVIDERS = {
    "Sarvam": "https://api.sarvam.ai/v2",
    "Local (free)": "http://ollama:11434/v1",
}

# Frozen copy of app/services/extra_models.py at the time of this migration.
# provider: [(name, display name, description, context window, is latest)]
MODELS = {
    "Sarvam": [
        ("sarvam-105b", "Sarvam 105B", "Indian model, strongest in Hindi and Indian languages", 128000, True),
        ("sarvam-105b-conversations", "Sarvam 105B Conversations", "Sarvam 105B tuned for dialogue", 32000, True),
        ("glm5.3-flash", "GLM 5.3 Flash (Sarvam)", "Lowest-cost chat on Sarvam", 1000000, False),
        ("gemma4", "Gemma 4 31B (Sarvam)", "Fast answers", 256000, False),
        ("deepseekv4.1-flash-1017", "DeepSeek V4.1 Flash (Sarvam)", "General chat", 1000000, False),
    ],
    "Local (free)": [
        ("gpt-oss:20b", "GPT-OSS 20B (free, on this server)", "OpenAI open-weight model, runs here at no cost", 32000, True),
        ("hf.co/bartowski/sarvamai_sarvam-m-GGUF:Q4_K_M", "Sarvam-M (free, on this server)",
         "Indian open-weight model, Hindi and Indian languages, runs here at no cost", 32000, True),
    ],
}


def upgrade() -> None:
    conn = op.get_bind()
    meta = sa.MetaData()
    api_provider = sa.Table("api_provider", meta, autoload_with=conn)
    ai_model = sa.Table("ai_model", meta, autoload_with=conn)

    # A new install has no providers yet; seed_defaults fills it.
    if conn.execute(sa.select(api_provider.c.id).limit(1)).first() is None:
        return

    for name, base_url in PROVIDERS.items():
        row = conn.execute(sa.select(api_provider.c.id).where(api_provider.c.name == name)).first()
        if row is None:
            conn.execute(api_provider.insert().values(name=name, is_active=True, base_url=base_url))
        provider_id = conn.execute(sa.select(api_provider.c.id).where(api_provider.c.name == name)).scalar()
        for order, (model, display, description, context, latest) in enumerate(MODELS[name], 1):
            exists = conn.execute(sa.select(ai_model.c.id).where(
                ai_model.c.provider_id == provider_id, ai_model.c.name == model)).first()
            if exists:
                continue
            conn.execute(ai_model.insert().values(
                name=model, display_name=display, description=description, provider_id=provider_id,
                context_window=context, is_latest=latest, sort_order=order, is_active=True,
                created_at=datetime.utcnow()))


def downgrade() -> None:
    """Not used: going back means restoring the backup taken before the upgrade."""
