from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator

class SurveySubmission(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=13, le=120)
    consent: bool
    rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = Field(None, max_length=1000)

    @field_validator("consent")
    def consent_must_be_true(cls, v):
        if not v:
            raise ValueError("consent must be true")
        return v

    @field_validator("comments")
    def comments_not_blank(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("comments cannot be empty")
        return v

class StoredSurveyRecord(SurveySubmission):
    received_at: datetime
    ip: str