"""OAuth token management for Gmail."""

import json
import logging
from pathlib import Path
from typing import Sequence, cast

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

GMAIL_READONLY_SCOPE = "https://www.googleapis.com/auth/gmail.readonly"

logger = logging.getLogger(__name__)


class TokenManager:
    """Manages Gmail OAuth2 tokens with automatic refresh and persistence."""

    def __init__(self, credentials_path: str, token_path: str) -> None:
        self.credentials_path = Path(credentials_path)
        self.token_path = Path(token_path)

    def get_credentials(self, scopes: Sequence[str] | None = None) -> Credentials:
        """Load credentials or run OAuth flow, then persist token.

        Args:
            scopes: OAuth scopes to request. Defaults to Gmail read-only.

        Returns:
            Credentials: Valid Gmail OAuth credentials.

        Raises:
            FileNotFoundError: If credentials.json is missing.
        """
        if not self.credentials_path.exists():
            raise FileNotFoundError(
                f"Missing OAuth credentials file: {self.credentials_path}. "
                "Download credentials.json from Google Cloud Console."
            )

        scopes = list(scopes or [GMAIL_READONLY_SCOPE])

        creds = self._load_token(scopes)
        if creds and creds.valid:
            return creds

        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing expired Gmail token")
            creds.refresh(Request())
            refreshed = cast(Credentials, creds)
            self._save_token(refreshed)
            return refreshed

        logger.info("Starting Gmail OAuth flow")
        flow = InstalledAppFlow.from_client_secrets_file(
            str(self.credentials_path),
            scopes=scopes,
        )
        creds = cast(Credentials, flow.run_local_server(port=0))
        self._save_token(creds)
        return creds

    def _load_token(self, scopes: Sequence[str]) -> Credentials | None:
        if not self.token_path.exists():
            return None

        try:
            creds = Credentials.from_authorized_user_file(str(self.token_path), scopes=scopes)
            return cast(Credentials, creds)
        except (ValueError, json.JSONDecodeError) as exc:
            logger.warning("Invalid token.json, re-auth required: %s", exc)
            return None

    def _save_token(self, creds: Credentials) -> None:
        self._ensure_token_dir()
        token_data = {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": creds.scopes,
        }
        self.token_path.write_text(json.dumps(token_data, indent=2))
        logger.info("Token saved to %s", self.token_path)

    def _ensure_token_dir(self) -> None:
        if self.token_path.parent == Path("."):
            return
        self.token_path.parent.mkdir(parents=True, exist_ok=True)

    def health_check(self) -> tuple[bool, str]:
        try:
            creds = self.get_credentials()
            if creds.expired:
                return False, "Token expired"
            return True, "Credentials valid"
        except FileNotFoundError:
            return False, "Credentials file not found"
        except Exception as exc:  # pragma: no cover - defensive
            return False, f"Health check error: {exc}"
