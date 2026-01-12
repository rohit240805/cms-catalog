import threading

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.worker import run as worker_run

from app.routers import (
    health,
    auth,
    programs,
    terms,
    lessons,
    admin,
    catalog,
)

app = FastAPI(title="CMS + Catalog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ START BACKGROUND WORKER ON APP STARTUP
@app.on_event("startup")
def start_background_worker():
    thread = threading.Thread(
        target=worker_run,
        daemon=True
    )
    thread.start()
    print("🚀 Background worker thread started")

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(programs.router)
app.include_router(terms.router)
app.include_router(lessons.router)
app.include_router(admin.router)
app.include_router(catalog.router)
