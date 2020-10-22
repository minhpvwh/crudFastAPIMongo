import uvicorn
from configs import port, reloadMode, host

if __name__ == "__main__":
    uvicorn.run("server.app:app", host=host, port=port, reload=reloadMode)
