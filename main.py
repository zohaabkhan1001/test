import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from routes.api import router as api_router

app = FastAPI()

origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code,
                        content={
                            "data": {},
                            "success": True if exc.status_code == 200 else False,
                            "status_code": exc.status_code,
                            "message": exc.detail
                        })


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(status_code=500,
                        content={
                            "data": {},
                            "success": False,
                            "status_code": 500,
                            "message": "Internal Server Error"
                        })


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=404,
                        content={
                            "data": {},
                            "success": False,
                            "status_code": 404,
                            "message": "Not Found"
                        })


if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, log_level="info", reload=True)
    print("running")
