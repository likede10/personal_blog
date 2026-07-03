from fastapi import APIRouter

router_login = APIRouter(prefix="/login", tags=["login"])


@router_login.post('/register')
async def register():
    return {"data": "register success"}