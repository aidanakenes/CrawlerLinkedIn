import uvicorn

from fastapi import FastAPI, Request, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.models.user import User
from src.service.crawler_user import LICrawler
from src.service.collector import IDCollector
from src.utils.err_utils import ApplicationError, NotFoundError, ValidationError

app = FastAPI()


@app.get('/linkedin/profile', description='Get profile info')
async def get(user_id: str):
    try:
        crawler = LICrawler()
        _user: User = crawler.get_user_by_id(user_id=user_id)
    except NotFoundError or ApplicationError as e:
        return JSONResponse(
            status_code=e.code,
            content=jsonable_encoder({'error': e})
        )
    return JSONResponse(
        content=jsonable_encoder({'data': _user})
    )


@app.get('/linkedin/search')
async def get(fullname: str):
    assert len(fullname.split()) > 1
    try:
        _users = []
        collector = IDCollector()
        _users_id = collector.collect_id(fullname=fullname)
        if len(_users_id) >= 1:
            crawler = LICrawler()
            for user_id in _users_id:
                _users.append(crawler.get_user_by_id(user_id))
    except NotFoundError or ApplicationError as e:
        return JSONResponse(
            status_code=e.code,
            content=jsonable_encoder({'error': e})
        )
    return JSONResponse(
        content=jsonable_encoder({'total': len(_users), 'data': _users})
    )


@app.exception_handler(AssertionError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=ValidationError().code,
        content=jsonable_encoder({'error': ValidationError()})
    )


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8080, workers=4)
