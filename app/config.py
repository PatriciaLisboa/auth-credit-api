import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()  # carrega variáveis do arquivo .env

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Admin domain for automatic admin role assignment
ADMIN_DOMAIN = os.getenv("ADMIN_DOMAIN", "@admin.example.com")