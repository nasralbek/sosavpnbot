import os
import uvicorn



if __name__ == "__main__":
    reload_flag = os.getenv("FASTAPI_RELOAD", "false").lower() == "true"
    uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8000,
    reload=reload_flag,
    log_level="trace",
)
