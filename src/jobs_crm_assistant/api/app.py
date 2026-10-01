"""Main FastAPI application module."""
from typing import Dict, Sequence

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from jobs_crm_assistant.core.config import CorsSettings


def create_app(cors_origins: Sequence[str]) -> FastAPI:
    """Build the application, allowing browser calls only from cors_origins."""
    app = FastAPI(
        title="Jobs CRM Assistant",
        description="AI-powered CRM Assistant for job applications",
        version="0.1.0",
    )

    # Configure CORS. A wildcard origin never gets credentials: with both,
    # Starlette echoes any caller's origin and lets every site use the
    # user's cookies.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(cors_origins),
        allow_credentials="*" not in cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    async def health_check() -> Dict[str, str]:
        """Health check endpoint."""
        return {"status": "healthy"}

    return app


app = create_app(CorsSettings().cors_origins)
