from fastapi import FastAPI, responses
from auth.controllers import auth_router
from users.controllers import profile_router
from jobs.controllers import jobs_router
from company.controllers import company_router
from education.controllers import education_router
from auth.social_auth.controllers import social_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(default_response_class=responses.ORJSONResponse)

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(jobs_router)
app.include_router(company_router)
app.include_router(education_router)
app.include_router(social_router)

origins = ['http://127.0.0.1:8000']

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
