from pydantic import BaseModel, Field
from typing import List, Optional

class Experience(BaseModel):
    """Individual work experience entry"""
    job_title: str = Field(
        ...,
        description="Job title or position held"
    )
    company: str = Field(
        ...,
        description="Company or organization name"
    )
    duration: str = Field(
        ...,
        description="Duration of employment (e.g., 'Jan 2020 - Present', '2 years')"
    )
    key_responsibilities: List[str] = Field(
        default=[],
        description="List of key responsibilities and achievements"
    )

class Education(BaseModel):
    """Educational background entry"""
    degree: str = Field(
        ...,
        description="Degree or certification obtained"
    )
    institution: str = Field(
        ...,
        description="Educational institution name"
    )
    year: Optional[str] = Field(
        default=None,
        description="Graduation year or completion date"
    )

class Project(BaseModel):
    """Individual project entry"""
    name: str = Field(
        ...,
        description="Project name or title"
    )
    description: str = Field(
        ...,
        description="Brief description of the project"
    )
    technologies: List[str] = Field(
        default=[],
        description="Technologies or tools used in the project"
    )

class ContactInfo(BaseModel):
    """Contact information from resume"""
    email: Optional[str] = Field(default=None, description="Email address")
    phone: Optional[str] = Field(default=None, description="Phone number")
    location: Optional[str] = Field(default=None, description="Current location")
    linkedin: Optional[str] = Field(default=None, description="LinkedIn profile URL")
    github: Optional[str] = Field(default=None, description="GitHub profile URL")
    portfolio: Optional[str] = Field(default=None, description="Portfolio website URL")

class Summary(BaseModel):
    """Complete resume summary extraction model"""
    
    # Personal Information
    full_name: Optional[str] = Field(
        default=None,
        description="Full name of the candidate"
    )
    
    contact_info: ContactInfo = Field(
        default_factory=ContactInfo,
        description="Contact information extracted from resume"
    )
    
    # Professional Summary
    professional_summary: str = Field(
        ...,
        description="A concise 2-3 sentence professional summary highlighting key qualifications"
    )
    
    # Skills
    technical_skills: List[str] = Field(
        default=[],
        description="List of technical skills, programming languages, frameworks, and tools"
    )
    
    soft_skills: List[str] = Field(
        default=[],
        description="List of soft skills and interpersonal abilities"
    )
    
    # Experience
    work_experience: List[Experience] = Field(
        default=[],
        description="List of work experiences in reverse chronological order"
    )
    
    total_experience: Optional[str] = Field(
        default=None,
        description="Total years of professional experience (e.g., '3+ years', '5 years')"
    )
    
    # Education
    education: List[Education] = Field(
        default=[],
        description="Educational background and qualifications"
    )
    
    # Projects
    notable_projects: List[Project] = Field(
        default=[],
        description="Key projects that demonstrate skills and experience"
    )
    
    # Additional Information
    certifications: List[str] = Field(
        default=[],
        description="Professional certifications and licenses"
    )
    
    achievements: List[str] = Field(
        default=[],
        description="Notable achievements, awards, or recognitions"
    )
    
    # Career targeting
    target_roles: List[str] = Field(
        default=[],
        description="Types of roles the candidate appears qualified for"
    )
    
    career_level: Optional[str] = Field(
        default=None,
        description="Career level: 'Entry Level', 'Mid Level', 'Senior Level', or 'Executive'"
    )