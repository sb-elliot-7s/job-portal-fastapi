from enum import Enum


class UserTypeEnum(str, Enum):
    RECRUITER = 'RECRUITER'
    EMPLOYEE = 'EMPLOYEE'


class Gender(str, Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'


class SpecializationEnum(str, Enum):
    BACKEND = 'BACKEND'
    FRONTEND = 'FRONTEND'
    DESIGN = 'DESIGN'
    SOFTWARE_DEVELOPMENT = 'SOFTWARE_DEVELOPMENT'
    ADMINISTRATION = 'ADMINISTRATION'
    MANAGEMENT = 'MANAGEMENT'
    SALES = 'SALES'
    MARKETING = 'MARKETING'


class SkillLevel(str, Enum):
    INTERN = 'INTERN'
    JUNIOR = 'JUNIOR'
    MIDDLE = 'MIDDLE'
    SENIOR = 'SENIOR'


class EmploymentType(str, Enum):
    PART_TIME = 'PART_TIME'
    FULL_TIME = 'FULL_TIME'
