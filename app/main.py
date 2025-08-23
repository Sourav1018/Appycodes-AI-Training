from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router as api_router
from app.db.qdrant_conn import close_qdrant_client, get_qdrant_client
from app.db.supabase_conn import close_supabase_client, get_supabase_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code can go here
    get_supabase_client()
    get_qdrant_client()
    yield
    # Shutdown code can go here
    close_qdrant_client()
    close_supabase_client()


app = FastAPI(lifespan=lifespan)


# Mount your routes
app.include_router(api_router, prefix="/api/v2")
