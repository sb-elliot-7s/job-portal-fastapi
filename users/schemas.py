from datetime import date, datetime
from typing import Optional
from fastapi import Form
from pydantic import BaseModel, Field
from common_enums import Gender
from auth.schemas import BaseUserAccountSchema
from education.schemas import EducationSchema
from common_enums import SkillLevel


class CreateExperienceSchema(BaseModel):
    job_title: Optional[str] = Field(max_length=200)
    job_description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    company_name: Optional[str] = Field(None, max_length=200)
    job_location: Optional[str]


class ExperienceSchema(CreateExperienceSchema):
    id: int
    user_account_id: int

    class Config:
        orm_mode = True


class CreateUserSkillSchema(BaseModel):
    skill_name: str = Field(max_length=100)


class UserSkillSchema(CreateUserSkillSchema):
    id: int
    user_account_id: int

    class Config:
        orm_mode = True


class CreateProfileSchema(BaseModel):
    username: Optional[str]
    first_name: Optional[str] = Field(max_length=100)
    last_name: Optional[str] = Field(max_length=100)
    nationality: Optional[str] = Field(None, max_length=100)
    contact_number: Optional[int]
    gender: Optional[Gender]
    date_of_birth: Optional[date]
    current_salary: Optional[float]
    currency: Optional[str] = Field(None, max_length=50)
    skill_level: Optional[SkillLevel] = SkillLevel.JUNIOR

    @classmethod
    def as_form(cls, username: Optional[str] = Form(None), first_name: str = Form(None), last_name: str = Form(None),
                nationality: Optional[str] = Form(None), contact_number: Optional[int] = Form(None),
                gender: Optional[Gender] = Form(None), date_of_birth: Optional[date] = Form(None),
                current_salary: Optional[float] = Form(None), currency: Optional[str] = Form(None),
                skill_level: Optional[SkillLevel] = Form(None)):
        return cls(username=username, first_name=first_name, last_name=last_name, nationality=nationality,
                   contact_number=contact_number, gender=gender, date_of_birth=date_of_birth, current_salary=current_salary,
                   currency=currency, skill_level=skill_level)


class ProfileSchema(BaseUserAccountSchema, CreateProfileSchema):
    id: int
    is_active: bool
    registration_date: datetime
    updated: datetime
    user_type_id: int
    user_image_url: Optional[str]
    educations: Optional[list[EducationSchema]]
    experiences: Optional[list[ExperienceSchema]]
    skills: Optional[list[UserSkillSchema]]

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda v: v.strftime('%Y-%m-%d %H:%M')}
        use_enum_values = True
