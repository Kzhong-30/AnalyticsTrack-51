from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import engine, Base
from .api import auth, users, lawyers, consultations, appointments, documents, knowledge, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(lawyers.router, prefix="/api")
app.include_router(consultations.router, prefix="/api")
app.include_router(appointments.router, prefix="/api")
app.include_router(documents.router, prefix="/api")
app.include_router(knowledge.router, prefix="/api")
app.include_router(admin.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "欢迎使用法律咨询平台 API"}
