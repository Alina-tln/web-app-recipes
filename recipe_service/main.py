from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import uvicorn

from recipe_service.routers.ingredients import category_router, ingredient_router
from recipe_service.core.dependencies import logger
from recipe_service.routers.recipes import recipe_router

# ----------------------------------------------------------
# Initializing the Application
# ----------------------------------------------------------
app = FastAPI(
    title="Recipe Service API",
    description="API for managing recipes and ingredients",
    version="1.0.0"
)


# ----------------------------------------------------------
# SQLAlchemy Global Error Interception Middleware
# ----------------------------------------------------------
@app.middleware("http")
async def db_error_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error on {request.method} {request.url}: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal database error"}
        )
    except Exception as e:
        logger.exception(f"Unexpected error on {request.method} {request.url}: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

app.include_router(category_router.router, tags=["Categories"])
app.include_router(ingredient_router.router, tags=["Ingredients"])
app.include_router(recipe_router.router, tags=["Recipes"])


# ----------------------------------------------------------
# Entrypoint (dev only)
# ----------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("recipe_service.main:app", reload=True)
