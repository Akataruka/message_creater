from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

class UserInput(BaseModel):
    summary: str = Field(
        ...,
        description="A short summary or bio of the user, typically derived from a resume."
    )
    resume: Optional[str] = Field(
        default="",
        description="URL to the user's resume."
    )
    linkedin: Optional[str] = Field(
        default="",
        description="URL to the user's LinkedIn profile."
    )
    github: Optional[str] = Field(
        default="",
        description="URL to the user's GitHub profile."
    )
    portfolio: Optional[str] = Field(
        default="",
        description="URL to the user's personal portfolio or website."
    )
    blog: Optional[str] = Field(
        default="",
        description="URL to the user's personal blog or website."
    )
    message_type: str = Field(
        ...,
        description="The type of message to generate, e.g., 'Cold Email', 'LinkedIn Message', or 'Other'."
    )
    job_type: str = Field(
        ...,
        description="The type of job or position being targeted, e.g., 'Software Developer', 'Data Scientist', etc."
    )
    
    
class LinkMap(BaseModel):
    linkedin: Optional[HttpUrl] = Field(
        default=None,
        description="URL to the user's LinkedIn profile"
    )
    github: Optional[HttpUrl] = Field(
        default=None,
        description="URL to the user's GitHub profile"
    )
    portfolio: Optional[HttpUrl] = Field(
        default=None,
        description="URL to the user's portfolio website"
    )
    blog: Optional[HttpUrl] = Field(
        default=None,
        description="URL to the user's blog site eg. Hashnode or Dev.to or Medium"
    )
