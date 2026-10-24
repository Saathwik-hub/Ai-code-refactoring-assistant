import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.routes.auth import router as auth_router
from backend.routes.files import router as files_router
from backend.routes.syntax import router as syntax_router
from backend.routes.analysis_routes import router as analysis_router
from backend.routes.ai_routes import router as ai_router
from backend.routes.optimizer_routes import router as optimizer_router

# Initialize SQLite database tables
from backend.database import init_db
init_db()

app = FastAPI(
    title="AI Code Refactoring Assistant",
    description="Full-stack developer tool with Monaco Editor, Static Code Analysis, AI Refactoring Engine, Side-by-Side Diff Viewer, and Chat Assistant.",
    version="3.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers (Phase 1 + Phase 2 + Phase 3 + Optimizer)
app.include_router(auth_router)
app.include_router(files_router)
app.include_router(syntax_router)
app.include_router(analysis_router)
app.include_router(ai_router)
app.include_router(optimizer_router)

# Mount Frontend static files at root '/' with html=True
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

@app.get("/health")
def health_check():
    return {"status": "healthy", "phase": "3-AI-Refactoring"}

if __name__ == "__main__":
    import uvicorn
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.app:app", host=host, port=port, reload=True)
