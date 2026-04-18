from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.bootstrap import ensure_default_admin
from app.routes import auth, categories, colors, orders, products, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    ensure_default_admin()
    yield
    # Shutdown
    pass


app = FastAPI(lifespan=lifespan)

app.add_middleware(
	CORSMiddleware,
	allow_origins=[
		"http://localhost:5173",
		"http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
	],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(colors.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(orders.admin_router)