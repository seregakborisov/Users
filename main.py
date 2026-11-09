import time

from fastapi import FastAPI, Request

from db.main import init_models

from handlers import router

app = FastAPI()


@app.on_event("startup")
async def startup():
    await init_models()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(router)
