from passlib.context import CryptContext
from core.config import get_settings
from fastapi.security import OAuth2PasswordBearer

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")