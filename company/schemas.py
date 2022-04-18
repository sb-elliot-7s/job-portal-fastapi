from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl
from fastapi import Form
from common_enums import SpecializationEnum
from jobs.schemas import JobSchema


class CompanyImageSchema(BaseModel):
    id: int
    company_id: int
    photo_url: str

    class Config:
        orm_mode = True


class CreateSpecializationSchema(BaseModel):
    specialization_name: SpecializationEnum


class SpecializationSchema(CreateSpecializationSchema):
    id: int

    class Config:
        orm_mode = True


class CreateCompanySchema(BaseModel):
    company_name: str = Field(max_length=200)
    profile_description: str
    country: str
    city: str = Field(max_length=255)
    street: Optional[str] = Field(max_length=255)
    house_number: Optional[str] = Field(max_length=10)
    company_website_url: Optional[HttpUrl]

    @classmethod
    def as_form(cls, company_name: str = Form(...), profile_description: str = Form(...), country: str = Form(...),
                city: str = Form(...), street: Optional[str] = Form(None), house_number: Optional[str] = Form(None),
                company_website_url: Optional[HttpUrl] = Form(None)):
        return cls(company_name=company_name, profile_description=profile_description,
                   country=country, city=city, street=street, house_number=house_number, company_website_url=company_website_url)


class CompanySchema(CreateCompanySchema):
    id: int
    created_date: datetime
    user_account_id: int
    jobs: list[JobSchema]
    company_images: list[CompanyImageSchema]
    specializations: list[SpecializationSchema]

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda v: v.strftime('%Y-%m-%d %H:%M')}
