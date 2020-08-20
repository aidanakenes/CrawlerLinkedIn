from http import HTTPStatus

import uvicorn
from fastapi import FastAPI, Request, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.api.publisher import Publisher
from src.utils.task_manager import TaskManager, Task
from src.api.searcher import Searcher
from src.utils.err_utils import ValidationError, IDValidationError, CustomException, DoesNotExist

app = FastAPI()
task_manager = TaskManager()


@app.get('/linkedin/profile')
async def get(user_id: str = Query(..., min_length=1, max_length=128, regex='^[a-z0-9-]{1,128}$')):
    task = task_manager.get_task(endpoint='profile', keywords=user_id)
    if task is None:
        with Publisher() as publisher:
            publisher.publish_to_crawler_id(
                user_id=user_id,
                endpoint='profile',
                keywords=user_id,
                last=None
            )
        return JSONResponse(
            status_code=HTTPStatus.CREATED,
            content=jsonable_encoder({'message': 'Keep calm, response in progress!'})
        )
    if task.status == 'done':
        user = Searcher().get_user_by_id(user_id=user_id)
        return JSONResponse(
            content=jsonable_encoder({'data': user})
        )
    else:
        content, status_code = task_manager.task_status(task)
        return JSONResponse(status_code=status_code, content=jsonable_encoder(content))


@app.get('/linkedin/search')
async def get(fullname: str):
    if len(fullname.split()) <= 1:
        raise ValidationError()
    task = task_manager.get_task(endpoint='search', keywords=fullname)
    if task is None:
        with Publisher() as publisher:
            publisher.publish_to_crawler_fullname(fullname=fullname)
        return JSONResponse(
            status_code=HTTPStatus.CREATED,
            content=jsonable_encoder({'message': 'Keep calm, response in progress!'})
        )
    last_id = task.last
    last_user = Searcher().get_user_by_id(last_id)
    if last_id is None or last_user is None:
        return JSONResponse(
            status_code=HTTPStatus.CREATED,
            content=jsonable_encoder({'message': 'Keep calm, response in progress!'})
        )
    if last_user:
        users = Searcher().get_users_by_fullname(fullname)
        task_manager.update_status(task, 'done')
        return JSONResponse(
            content=jsonable_encoder({'total': len(users), 'data': users})
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
    uvicorn.run('api:app', host='0.0.0.0', port=8080, workers=4)
