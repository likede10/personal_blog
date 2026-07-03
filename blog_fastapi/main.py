from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware




# router
from router.login import router_login
app = FastAPI()

app.include_router(router_login)

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # 允许的源
    allow_credentials=True, # 允许携带 cookie
    allow_methods=["*"], # 允许的请求方法
    allow_headers=["*"], # 允许的请求头
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/test")
async def test():
    return {"message": "test"}
