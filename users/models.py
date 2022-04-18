from common_enums import Gender, SkillLevel

from database import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from common_enums import UserTypeEnum

from company.models import Company


class UserAccount(Base):
    __tablename__ = 'user_account'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String(length=100))
    email = sa.Column(sa.String, unique=True)
    password = sa.Column(sa.String)
    first_name = sa.Column(sa.String(length=100), nullable=True)
    last_name = sa.Column(sa.String(length=100), nullable=True)
    nationality = sa.Column(sa.String(length=100))
    contact_number = sa.Column(sa.Integer)
    gender = sa.Column(ENUM(Gender, name='gender_type', create_type=False), default=Gender.MALE.value)
    date_of_birth = sa.Column(sa.Date)
    current_salary = sa.Column(sa.Numeric(12, 2))
    currency = sa.Column(sa.String(length=50), nullable=True)
    user_image_url = sa.Column(sa.String)
    skill_level = sa.Column(ENUM(SkillLevel, name='skill_level_v'))
    is_active = sa.Column(sa.Boolean, default=True)
    registration_date = sa.Column(sa.DateTime, default=sa.func.now())
    updated = sa.Column(sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())
    user_type_id = sa.Column(sa.Integer, sa.ForeignKey('user_type.id', ondelete='CASCADE'))

    skills = relationship('UserSkill', backref='user_account', lazy='joined', passive_deletes=True)
    educations = relationship('Education', backref='user_account', lazy='joined', passive_deletes=True)
    company = relationship('Company', backref='user_account', uselist=False, lazy='joined', passive_deletes=True)
    experiences = relationship('Experience', backref='user_account', lazy='joined', passive_deletes=True)
    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self) -> str:
        return f'<User: {self.username} {self.first_name} {self.email}>'


class UserType(Base):
    __tablename__ = 'user_type'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    user_type_value = sa.Column(ENUM(UserTypeEnum, name='user_type_value', create_type=False))

    user_accounts = relationship('UserAccount', backref='user_type', passive_deletes=True)

    def __repr__(self) -> str:
        return f'<UserType: {self.user_type_name}>'


class UserSkill(Base):
    __tablename__ = 'user_skill'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    skill_name = sa.Column(sa.String(length=100))
    user_account_id = sa.Column(sa.Integer, sa.ForeignKey('user_account.id', ondelete='CASCADE'))

    def __repr__(self) -> str:
        return f'User Skill: {self.skill_name}'


class Experience(Base):
    __tablename__ = 'experience'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    user_account_id = sa.Column(sa.Integer, sa.ForeignKey('user_account.id', ondelete='CASCADE'))
    job_title = sa.Column(sa.String(length=200))
    job_description = sa.Column(sa.String, nullable=True)
    start_date = sa.Column(sa.Date)
    end_date = sa.Column(sa.Date)
    company_name = sa.Column(sa.String(length=200), nullable=True)
    job_location = sa.Column(sa.String, nullable=True)

    def __repr__(self) -> str:
        return f'Experience Detail: {self.job_title}'
