from fastapi import FastAPI, APIRouter
from appv1.routers import users, categorys, transactions
from core.config import settings


api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(categorys.router, prefix="/categorys", tags=["categorys"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, description=settings.PROJECT_DESCRIPTION)
app.include_router(api_router)

