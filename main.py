from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import FileResponse
from app.routers import scheduler
import os

app = FastAPI(
    title="Jun's Portfolio Hub",
    description="Central Hub for all AI Projects",
    version="1.0.0"
)

# 1. Mount Shared Static Files
#    This allows all sub-apps to access /static/style.css etc.
#    Since project_scheduler's index.html uses /static, it typically resolves to default host/static
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 2. Mount Sub-Applications / Routers
#    Mount at /scheduler prefix
app.include_router(scheduler.router, prefix="/scheduler", tags=["scheduler"])

# 3. Serve Portfolio Landing Page
@app.get("/")
def read_root():
    return FileResponse('static/portfolio.html')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_portfolio:app", host="127.0.0.1", port=8000, reload=True)
