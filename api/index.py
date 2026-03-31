import traceback
try:
    from app.main import app
except Exception as e:
    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse
    
    app = FastAPI()
    
    @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    def catch_all(path: str):
        return PlainTextResponse("Hello from fallback! Error: " + traceback.format_exc(), status_code=200)
