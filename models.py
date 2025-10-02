from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator

class SurveySubmission(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=13, le=120)
    consent: bool
    rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = Field(None, max_length=1000)

    @validator("comments")
    def strip_comments(cls, v):
        if v is not None:
            v = v.strip()
            if v == "":
                raise ValueError("comments cannot be empty")
        return v

    @validator("consent")
    def must_consent(cls, v):
        if v is not True:
            raise ValueError("consent must be true")
        return v


class StoredSurveyRecord(SurveySubmission):
    received_at: datetime
    ip: str