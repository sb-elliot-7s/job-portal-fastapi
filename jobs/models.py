import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from common_enums import EmploymentType, SpecializationEnum
from database import Base


class Job(Base):
    __tablename__ = 'job'
    posted_by_id = sa.Column(sa.Integer, sa.ForeignKey('user_account.id', ondelete='CASCADE'))
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    company_id = sa.Column(sa.Integer, sa.ForeignKey('company.id', ondelete='CASCADE'))
    title = sa.Column(sa.String(length=255))
    job_description = sa.Column(sa.String)
    specialization_name = sa.Column(ENUM(SpecializationEnum, name='field_of_activity_job', create_type=False))
    created_date = sa.Column(sa.DateTime, default=sa.func.now())
    is_active = sa.Column(sa.Boolean, default=True)
    employment_type = sa.Column(ENUM(EmploymentType, name='employment_type', create_type=False))
    is_remote = sa.Column(sa.Boolean, default=False)
    country = sa.Column(sa.String(length=200), nullable=False)
    region = sa.Column(sa.String(length=200), nullable=False)
    city = sa.Column(sa.String(length=200), nullable=False)
    street = sa.Column(sa.String(length=200))

    job_skills = relationship('JobSkillSet', backref='job', lazy='joined', passive_deletes=True)

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self) -> str:
        return f'<Job: {self.title}>'


class JobSkillSet(Base):
    __tablename__ = 'job_skill'
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    job_id = sa.Column(sa.Integer, sa.ForeignKey('job.id', ondelete='CASCADE'))
    company_id = sa.Column(sa.Integer)
    skill_name = sa.Column(sa.String(length=100))

    def __repr__(self) -> str:
        return f'<Job Skill: {self.skill_set_name}>'
