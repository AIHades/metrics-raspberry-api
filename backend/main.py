import uvicorn

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from metrics import *
from api.routers.metrics_router import router as metrics_router


app = FastAPI()
app.include_router(metrics_router)

@app.get("/")
def redirect_to_metrics():
    return RedirectResponse("/metrics", status_code=301)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)