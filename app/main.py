from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_router, book_routes

app = FastAPI(title="Rezervacijų Sistema API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(book_routes.router)


@app.get("/")
def root():
    return {"status": "Aplikacija veikia sėkmingai!"}
