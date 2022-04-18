import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from common_enums import SpecializationEnum
from database import Base
from jobs.models import Job


class CompanyImage(Base):
    __tablename__ = 'company_image'
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    company_id = sa.Column(sa.Integer, sa.ForeignKey('company.id', ondelete='CASCADE'))
    photo_url = sa.Column(sa.String)

    def __repr__(self) -> str:
        return f'Company image: {self.photo_url}'


class Company(Base):
    __tablename__ = 'company'
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    company_name = sa.Column(sa.String(length=200), nullable=False)
    profile_description = sa.Column(sa.String, nullable=True)
    country = sa.Column(sa.String(length=100), nullable=False)
    city = sa.Column(sa.String(length=255), nullable=False)
    street = sa.Column(sa.String(length=255), nullable=True)
    house_number = sa.Column(sa.String(length=10), nullable=True)
    company_website_url = sa.Column(sa.String, nullable=True)
    created_date = sa.Column(sa.DateTime, default=sa.func.now())
    user_account_id = sa.Column(sa.Integer, sa.ForeignKey('user_account.id', ondelete='CASCADE'), unique=True)

    jobs = relationship('Job', backref='company', lazy='joined', passive_deletes=True)
    specializations = relationship('Specialization', backref='company', lazy='joined', passive_deletes=True)
    company_images = relationship(CompanyImage, backref='company', lazy='joined', passive_deletes=True)

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self) -> str:
        return f'<Company: {self.company_name}>'


class Specialization(Base):
    __tablename__ = 'specialization'
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    specialization_name = sa.Column(ENUM(SpecializationEnum, name='fields_activity_name'))
    company_id = sa.Column(sa.Integer, sa.ForeignKey('company.id', ondelete='CASCADE'))

    def __repr__(self) -> str:
        return f'<Field Of Activity: {self.field_of_activity_name}>'
