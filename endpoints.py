from enum import Enum


class Endpoint(str, Enum):
    # auth
    SIGN_UP = '/signup'
    LOGIN = '/login'
    REFRESH_TOKEN = '/refresh_token'
    # company
    COMPANY_ID = '/{company_id}'
    SPECIALIZATIONS = '/specializations'
    SPECIALIZATION_ID = '/specializations/{specialization_id}'
    ADD_IMAGE = '/images'
    IMAGES_ID = '/images/{image_id}'
    # education
    EDUCATION = '/'
    EDUCATION_ID = '/{education_id}'
    # job
    JOB = '/'
    JOB_ID = '/{job_id}'
    COMPANY_COMPANY_ID = '/company/{company_id}'
    JOB_SKILL_TO_JOB_ID = '/job_skills/{job_id}'
    JOB_SKILL_ID = '/job_skills/{skill_id}'
    # user_account
    EXPERIENCE = '/experience'
    EXPERIENCE_ID = '/experience/{experience_id}'
    PROFILE = '/'
    SKILLS = '/skills'
    SKILL_ID = '/skills/{skill_id}'
