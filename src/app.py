from typing import List

import uvicorn
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.models.user import User
from src.models.company import Company
from src.models.post import Post
from src.service.crawler_user import LIUserCrawler
from src.service.crawler_company import LICompanyCrawler
from src.service.crawler_post import LIPostCrawler
from src.utils.err_utils import ApplicationError

app = FastAPI()


@app.get('/profile', description='Get profile info')
async def get(user_url: str):
    try:
        parser = LIUserCrawler()
        # url = parse.urlparse(user_url)
        # print(url)
        _user: User = parser.get_user(user_url=user_url)
        return JSONResponse(
            content=jsonable_encoder({'data': _user})
        )
    except ApplicationError as e:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=jsonable_encoder({'error': type(e)})
        )


@app.get('/company', description='Get company info')
async def get(company_url: str):
    try:
        parser = LICompanyCrawler()
        _company: Company = parser.get_company(company_url=company_url)
        return JSONResponse(
            content=jsonable_encoder({'data': _company})
        )
    except ApplicationError as e:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=jsonable_encoder({'error': type(e)})
        )


@app.get('/posts', description='Get company\'s posts')
async def get(company_id: str):
    try:
        parser = LIPostCrawler()
        _posts: List[Post] = parser.get_posts(company_id=company_id)
        return JSONResponse(
            content=jsonable_encoder({'data': _posts})
        )
    except ApplicationError as e:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=jsonable_encoder({'error': type(e)})
        )


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8080, workers=4)
