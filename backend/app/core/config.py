from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/app/core/config.py -> project root (UseCase1/) that holds the reference PDFs/docx/xlsx
_REPO_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Application settings, loaded from environment variables / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str = "WTP Pension Prototyping Engine — Use Case 1"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # --- AI (Anthropic Claude) ---
    # Reads the key from ANTHROPIC_API_KEY or the ATP alias in backend/.env.
    ANTHROPIC_API_KEY: str | None = Field(
        default=None,
        validation_alias=AliasChoices("ANTHROPIC_API_KEY", "ATP"),
    )
    CLAUDE_MODEL: str = "claude-opus-4-8"
    # Per-document character cap fed to the model (keeps latency/cost bounded).
    MAX_DOC_CHARS: int = 60_000

    # --- RAG / vector search ---
    # Embedding backend: "azure" (Azure OpenAI text-embedding-3-large via the Foundry gateway)
    # or "local" (offline multilingual-e5). Azure = higher quality + scalable; local = offline.
    EMBED_BACKEND: str = "azure"
    # Local model (used when EMBED_BACKEND="local"): Dutch-capable, deterministic + offline.
    EMBED_MODEL: str = "intfloat/multilingual-e5-base"
    # Azure OpenAI embedding deployment name (used when EMBED_BACKEND="azure").
    AZURE_EMBED_DEPLOYMENT: str = "text-embedding-3-large"
    # Azure AI Foundry inference gateway (shared with the foundry-eu MCP). Reads FOUNDRY_ENDPOINT
    # / FOUNDRY_API_KEY from the environment / .env.
    FOUNDRY_ENDPOINT: str | None = None
    FOUNDRY_API_KEY: str | None = None
    # Chunking for document retrieval.
    CHUNK_SIZE: int = 900
    CHUNK_OVERLAP: int = 150

    # Directory that holds the built-in fund + benchmark source documents.
    DOCUMENTS_DIR: str = str(_REPO_ROOT)
    # Writable directory for user-uploaded documents + the metadata override store.
    UPLOADS_DIR: str = str(_REPO_ROOT / "uploads")

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.BACKEND_CORS_ORIGINS.split(",") if o.strip()]

    @property
    def documents_path(self) -> Path:
        return Path(self.DOCUMENTS_DIR)

    @property
    def uploads_path(self) -> Path:
        return Path(self.UPLOADS_DIR)

    @property
    def qdrant_path(self) -> Path:
        return Path(self.UPLOADS_DIR) / "_qdrant"

    @property
    def has_ai_credentials(self) -> bool:
        import os

        return bool(self.ANTHROPIC_API_KEY or os.environ.get("ANTHROPIC_API_KEY"))


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
