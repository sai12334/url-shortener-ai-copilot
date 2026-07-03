"""
Centralized application configuration.

Kept deliberately small and explicit rather than pulling in a settings
framework — this service has few enough config values that a dataclass-like
module is more readable than indirection through a Settings class.
"""
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./url_shortener.db")

# Length of generated short codes. 7 base62 chars gives 62^7 (~3.5 trillion)
# possible codes, which is a comfortable collision margin for this prototype.
SHORT_CODE_LENGTH = int(os.getenv("SHORT_CODE_LENGTH", "7"))

# Base URL used when composing the fully-qualified shortened link in API
# responses. In production this would come from environment/service config.
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

# Maximum attempts to generate a unique short code before giving up.
# Protects against an infinite loop if the code space were ever exhausted.
MAX_SHORT_CODE_GENERATION_ATTEMPTS = 5

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
