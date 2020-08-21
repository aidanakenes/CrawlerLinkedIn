from http import HTTPStatus

import uvicorn
from fastapi import FastAPI, Request, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.api.collector import IDCollector
from src.utils.task_manager import TaskManager, Task
from src.api.searcher import Searcher
from src.utils.err_utils import ValidationError, IDValidationError, QueryValidationError, CustomException, DoesNotExist

app = FastAPI()
task_manager = TaskManager()


@app.get('/linkedin/profile')
async def get(user_id: str = Query(..., min_length=1, max_length=128, regex='^[a-z0-9-]{1,128}$')):
    task_id = f'profile?{user_id}'
    task = task_manager.get_task(task_id)
    if task is None:
        with IDCollector() as collector:
            collector.publish_to_crawler_id(user_id)
        TaskManager().save_task(task=Task(
            task_id=task_id,
            status='in_progress',
            last=None
        ))
        return JSONResponse(
            status_code=HTTPStatus.CREATED,
            content=jsonable_encoder({'message': 'Keep calm, response in progress!'})
        )
    if task.status == 'done':
        user = Searcher().get_user_by_id(user_id=user_id)
        return JSONResponse(
            content=jsonable_encoder({'data': user})
        )

    if task.status == 'no':
        return JSONResponse(
            content=jsonable_encoder({'data': None})
        )
    if task.status == 'failed':
        return JSONResponse(
            status_code=CustomException().code,
            content=jsonable_encoder({'message': CustomException().message})
        )
    if task.status == 'in_progress':
        return JSONResponse(
            status_code=HTTPStatus.CREATED,
            content=jsonable_encoder({'message': 'Keep calm, response in progress!'})
        )


@app.get('/linkedin/search')
async def get(fullname: str):
    if len(fullname.split()) <= 1:
        raise ValidationError()
    task_id = f'search?{fullname}'
    task = task_manager.get_task(task_id)
    if task is None:
        try:
            with IDCollector() as collector:
                for user_id in collector.collect_id(fullname):
                    collector.publish_to_crawler_id(user_id)
                    last = user_id
            TaskManager().save_task(task=Task(
                task_id=task_id,
                status='in_progress',
                last=last
            ))
            return JSONResponse(
                status_code=HTTPStatus.CREATED,
                content=jsonable_encoder({'message': 'Keep calm, response in progress!'})
            )
        except DoesNotExist:
            return JSONResponse(
                content=jsonable_encoder({'data': None})
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
        content=jsonable_encoder({'error': exc.message})
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    req_dict = request.__dict__
    query = req_dict['scope']['query_string'].decode('utf-8')
    if 'user_id' not in query or 'fullname' not in query:
        return JSONResponse(
            status_code=QueryValidationError().code,
            content=jsonable_encoder({'error': QueryValidationError().message.format(query)})
        )
    return JSONResponse(
        status_code=IDValidationError().code,
        content=jsonable_encoder({'error': IDValidationError().message})
    )


if __name__ == '__main__':
    uvicorn.run('api:app', host='0.0.0.0', port=8080, workers=4)
