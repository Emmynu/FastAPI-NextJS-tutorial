from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.posts.routes import router
from contextlib import asynccontextmanager
from src.db.main import initDB
from src.auth.routes import router as authRouter
from src.reviews.routes import router as reviewRouter
from .middleware import add_middleware 

# To ensure our DB connects at the beginning of the program
@asynccontextmanager
async def lifeSpan(app:FastAPI):
    print("starting..")
    await initDB()
    yield
    print("stopping..")

# version of the program
version = "v1"

app = FastAPI(
    title="Postly",
    description="CRUD App",
    version=version,
    lifespan=lifeSpan
)

add_middleware(app=app)

# NB: Can have multiple api routers 
app.include_router(router, prefix="/api/{version}/posts", tags=["Posts"])
app.include_router(authRouter, prefix="/api/{version}/auth", tags=["Auth"])
app.include_router(reviewRouter, prefix="/api/{version}/reviews", tags=["Reviews"])

app.add_middleware(
    CORSMiddleware,
        allow_origins= ["http://localhost:3000", "https://fast-api-next-js-tutorial.vercel.app/"],
        allow_headers=["*"],
        allow_methods=["*"],
        allow_credentials=True
)

