from pydantic import BaseModel, HttpUrl, Field

class DealAnnotationCreate(BaseModel):
    """
    Data contract specifically for constructing an inbox Deal Annotation.
    """
    # Required Deal Properties
    description: str = Field(
        ..., 
        description="A short, compelling summary of your offer. Example: '20% off sitewide'"
    )
    discount_code: str = Field(
        ..., 
        description="The promo code a user applies at checkout. Example: '20TODAY'"
    )
    end_date_time: str = Field(
        ..., 
        description="The end date and time of the promotion in ISO 8601 format."
    )
    
    # Highly Recommended Properties
    start_date_time: str | None = Field(
        None, 
        description="The start date and time of the promotion in ISO 8601 format."
    )
    
    # Structural SFMC Assets (Kept as fallbacks/defaults for the other array objects)
    logo_url: str = Field("urlforlogo.png", description="The brand logo asset filename.")
    image_url: HttpUrl = Field(..., description="The preview visual banner asset link.")


class DealAnnotationResponse(BaseModel):
    """
    The output payload returned by the API containing the complete AMPscript block.
    """
    success: bool
    generated_ampscript_block: str