import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CreateEducationSchema(BaseModel):
    institute_university_name: str = Field(max_length=255)
    speciality: str = Field(max_length=255)
    start_date: datetime.date
    complete_date: datetime.date


class EducationSchema(CreateEducationSchema):
    id: int
    user_account_id: Optional[int]

    class Config:
        orm_mode = True
