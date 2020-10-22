from fastapi import FastAPI

from server.routes.student import router as StudentRouter
from server.routes.device import router as DeviceRouter

app = FastAPI()

app.include_router(StudentRouter, tags=["Student"], prefix="/student")
app.include_router(DeviceRouter, tags=["Device"], prefix="/device/v2")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
