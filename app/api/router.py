from fastapi import APIRouter
from app.api.v1 import email_annotations

api_router = APIRouter()

# Include the email annotations router under its own descriptive tag
api_router.include_router(
    email_annotations.router, 
    prefix="/email-annotations", 
    tags=["Email Annotations"]
)