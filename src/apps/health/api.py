from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix='/health',
    tags=['health'],
    default_response_class=JSONResponse,
)


@router.get('/ping')
async def ping() -> JSONResponse:
    return JSONResponse('pong')
