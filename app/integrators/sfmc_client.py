from datetime import datetime, timedelta
import httpx
from app.core.config import settings

class SFMCClient:
    """
    Integrator client dedicated to handling Salesforce Marketing Cloud 
    API communication and OAuth2 token lifecycles.
    """
    def __init__(self) -> None:
        # Ensure base URI doesn't have a trailing slash before appending paths
        self.auth_base_url = settings.AUTH_BASE_URI.rstrip("/")
        
        # In-memory storage for token caching
        self._cached_token: str | None = None
        self._token_expires_at: datetime = datetime.min

    async def get_access_token(self) -> str:
        """
        Retrieves a valid SFMC access token. Uses the cached token if it is still
        valid (minus a 60-second safety window), otherwise requests a fresh one.
        """
        now = datetime.utcnow()

        # Check if cache exists and is still fresh
        if self._cached_token and now < (self._token_expires_at - timedelta(seconds=60)):
            return self._cached_token

        # Cache is missing or expired -> Request a fresh token from the AUTH_BASE_URI
        token_endpoint = f"{self.auth_base_url}/v2/token"
        
        # Scenario A: Passing credentials in the body payload
        payload = {
            "grant_type": "client_credentials",
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.API_KEY  # Mapping API_KEY to secret slot
        }
        
        # Scenario B: Passing credentials in headers (Common gateway proxy requirement)
        headers = {
            "Content-Type": "application/json",
            "x-api-key": settings.API_KEY,
            "apikey": settings.API_KEY,
            "client_id": settings.CLIENT_ID
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(token_endpoint, json=payload, headers=headers)
                response.raise_for_status()
                
                token_data = response.json()
                self._cached_token = token_data["access_token"]
                
                # SFMC tokens typically last 1200 seconds (20 minutes)
                expires_in_seconds = token_data.get("expires_in", 1200)
                self._token_expires_at = datetime.utcnow() + timedelta(seconds=expires_in_seconds)
                
                # 💡 Defensive Type Guard: Asserts to the IDE that token is guaranteed to be a string
                if not self._cached_token:
                    raise RuntimeError("SFMC responded successfully but access_token field was empty.")
                
                return self._cached_token

            except httpx.HTTPStatusError as exc:
                raise RuntimeError(
                    f"SFMC OAuth failure: Gateway returned status code {exc.response.status_code} "
                    f"with details: {exc.response.text}"
                )
            except httpx.RequestError as exc:
                # Captures precise low-level connection drops (like bad URLs or proxy blocks)
                raise RuntimeError(
                    f"Network connection failed while routing to endpoint {exc.request.url}. "
                    f"Underlying details: {type(exc).__name__} - {str(exc)}"
                )
            except Exception as exc:
                raise RuntimeError(f"Unexpected parsing error: {str(exc)}")