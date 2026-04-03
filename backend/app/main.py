from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.bootstrap import ensure_default_admin
from app.routes import auth, categories, colors, orders, products, users

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=[
		"http://localhost:5173",
		"http://127.0.0.1:5173",
	],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

ensure_default_admin()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(colors.router)
app.include_router(products.router)
app.include_router(orders.router)