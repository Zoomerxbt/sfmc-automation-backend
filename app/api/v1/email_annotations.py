from fastapi import APIRouter, Depends, status
from app.schemas.email_annotations import DealAnnotationCreate, DealAnnotationResponse
from app.services.email_service import EmailAnnotationService
from app.integrators.sfmc_client import SFMCClient

router = APIRouter()

# 1. Instantiate the single shared instance of our client engine (Singleton)
sfmc_client = SFMCClient()

# 2. Dependency factory that feeds our client engine directly into the service layer
def get_email_service() -> EmailAnnotationService:
    return EmailAnnotationService(sfmc_client=sfmc_client)


# -------------------------------------------------------------------------
# Core Feature: Deal Annotation Generator
# -------------------------------------------------------------------------
@router.post(
    "/generate-deal", 
    response_model=DealAnnotationResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Generate a complete SFMC Deal Annotation Block"
)
async def generate_deal_annotation(
    payload: DealAnnotationCreate,
    service: EmailAnnotationService = Depends(get_email_service)
):
    """
    Receives promotional details, generates the AMPscript payload, 
    and is now fully wired into our live token token engine.
    """
    result = service.build_deal_annotation(payload)
    return result


# -------------------------------------------------------------------------
# Diagnostic Tool: Token Tester
# -------------------------------------------------------------------------
@router.get(
    "/test-token", 
    tags=["Diagnostic Tools"],
    summary="Fetch and verify real-time SFMC Access Token"
)
async def test_sfmc_token():
    """
    Diagnostic tool confirming that your absolute environment paths
    and gateway routing logic remain fully authenticated.
    """
    try:
        token = await sfmc_client.get_access_token()
        return {
            "status": "success",
            "access_token_preview": f"{token[:15]}...",
            "cached_until_utc": sfmc_client._token_expires_at.isoformat()
        }
    except Exception as e:
        return {
            "status": "failed", 
            "error_message": str(e)
        }