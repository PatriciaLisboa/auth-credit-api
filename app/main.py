from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from typing import List, Optional

from app.database import engine, Base
from app.routers import users, debts, score
from app.schemas import UserCreate, UserResponse, Token, Login, MessageResponse, DebtCreate, DebtResponse

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Credit System API", docs_url=None, redoc_url=None)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(debts.router)
app.include_router(score.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Credit System API"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Credit System API",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "persistAuthorization": True,
            "displayRequestDuration": True,
            "filter": True,
            "tryItOutEnabled": True
        }
    )

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Credit System API",
        version="1.0.0",
        description="API for managing credit scores and debt records",
        routes=app.routes,
    )
    
    # Add security scheme and schemas
    openapi_schema["components"] = {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Enter your JWT token in the format: Bearer <token>"
            }
        },
        "schemas": {
            "UserCreate": UserCreate.model_json_schema(),
            "UserResponse": UserResponse.model_json_schema(),
            "Token": Token.model_json_schema(),
            "Login": Login.model_json_schema(),
            "MessageResponse": MessageResponse.model_json_schema(),
            "DebtCreate": DebtCreate.model_json_schema(),
            "DebtResponse": DebtResponse.model_json_schema(),
            "ValidationError": {
                "type": "object",
                "properties": {
                    "loc": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "msg": {"type": "string"},
                    "type": {"type": "string"}
                },
                "required": ["loc", "msg", "type"]
            },
            "HTTPValidationError": {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/ValidationError"}
                    }
                },
                "required": ["detail"]
            }
        }
    }
    openapi_schema["security"] = [{"bearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi