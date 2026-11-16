"""Language models added by this fork: Sarvam's hosted API (Indian, paid on the Sarvam
key) and the free models served on this machine by Ollama.

One list, read by the seed for a new install and by migration 0004 for an existing one.
The Local names are Ollama tags pulled by the local AI service (see docker-compose.coolify.yaml).
"""

EXTRA_MODELS = [
    # Sarvam Token Factory, serverless (any key can call them).
    {"name": "sarvam-105b", "display_name": "Sarvam 105B", "provider": "Sarvam",
     "description": "Indian model, strongest in Hindi and Indian languages", "context_window": 128000, "is_latest": True},
    {"name": "sarvam-105b-conversations", "display_name": "Sarvam 105B Conversations", "provider": "Sarvam",
     "description": "Sarvam 105B tuned for dialogue", "context_window": 32000, "is_latest": True},
    {"name": "glm5.3-flash", "display_name": "GLM 5.3 Flash (Sarvam)", "provider": "Sarvam",
     "description": "Lowest-cost chat on Sarvam", "context_window": 1000000},
    {"name": "gemma4", "display_name": "Gemma 4 31B (Sarvam)", "provider": "Sarvam",
     "description": "Fast answers", "context_window": 256000},
    {"name": "deepseekv4.1-flash-1017", "display_name": "DeepSeek V4.1 Flash (Sarvam)", "provider": "Sarvam",
     "description": "General chat", "context_window": 1000000},
    # Free, on this server. Slower than the hosted models: a few words a second.
    # Param2 (BharatGen, Indian, 22 languages) first: about 6 words a second here, five
    # times GPT-OSS, because only 2.4B of its 17B parameters work per word.
    {"name": "param2-17b", "display_name": "BharatGen Param2 17B (free, on this server)", "provider": "Local (free)",
     "description": "Indian open-weight model, 22 Indian languages, the fastest free model here. Non-commercial use only",
     "context_window": 32000, "is_latest": True},
]
