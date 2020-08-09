import uvicorn
from fastapi import FastAPI, Request, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.service.collector import IDCollector
from src.service.crawler_user import LICrawler
from src.utils.err_utils import ValidationError, IDValidationError, CustomException

app = FastAPI()


@app.get('/linkedin/profile')
async def get(user_id: str = Query(..., min_length=1, max_length=128, regex='^[a-z0-9-]{1,128}$')):
    return JSONResponse(
        content=jsonable_encoder({'data': LICrawler().get_user_by_id(user_id=user_id)})
    )


@app.get('/linkedin/search')
async def get(fullname: str):
    if not len(fullname.split()) > 1:
        raise ValidationError()
    users_id = IDCollector().collect_id(fullname=fullname)
    _users = LICrawler().get_users_by_id(users_id=users_id)
    return JSONResponse(
        content=jsonable_encoder({'total': len(_users), 'data': _users})
    )


@app.exception_handler(CustomException)
async def exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=exc.code,
        content=jsonable_encoder({'error': exc})
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=IDValidationError().code,
        content=jsonable_encoder({'error': IDValidationError()})
    )


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8080, workers=4)
