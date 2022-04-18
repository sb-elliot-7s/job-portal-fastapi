from database import Base
import sqlalchemy as sa


class Education(Base):
    __tablename__ = 'education'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    user_account_id = sa.Column(sa.Integer, sa.ForeignKey('user_account.id', ondelete='CASCADE'))
    institute_university_name = sa.Column(sa.String(length=255))
    speciality = sa.Column(sa.String(length=255))
    start_date = sa.Column(sa.Date)
    complete_date = sa.Column(sa.Date)

    def __repr__(self) -> str:
        return f'<Education {self.institute_university_name} {self.speciality}>'
