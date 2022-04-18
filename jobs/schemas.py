from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from common_enums import SpecializationEnum, EmploymentType


class CreateJobSkillSchema(BaseModel):
    skill_name: str = Field(max_length=100)


class JobSkillSchema(CreateJobSkillSchema):
    id: int
    job_id: int
    company_id: int

    class Config:
        orm_mode = True


class CreateJobSchema(BaseModel):
    title: str = Field(max_length=255)
    job_description: str
    specialization_name: SpecializationEnum
    employment_type: EmploymentType
    is_remote: bool = Field(False)
    country: str = Field(..., max_length=200)
    region: str = Field(..., max_length=200)
    city: str = Field(..., max_length=200)
    street: Optional[str] = Field(None, max_length=200)


class JobSchema(CreateJobSchema):
    id: int
    posted_by_id: int
    company_id: int
    created_date: datetime
    is_active: bool
    job_skills: list[JobSkillSchema]

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda v: v.strftime('%Y-%m-%s %H:%m')}
