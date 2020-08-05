from typing import List

import uvicorn
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.models.user import User
from src.models.company import Company
from src.models.post import Post
from src.db.cache import Cache
from src.service.crawler_user import LIUserCrawler
from src.service.crawler_company import LICompanyCrawler
from src.service.crawler_post import LIPostCrawler
from src.utils.err_utils import ApplicationError

app = FastAPI()

my_redis = Cache()


@app.get('/profile', description='Get profile info')
async def get(user_id: str):
    _user = my_redis.get_cache_user(user_id=user_id)
    if _user is None:
        try:
            parser = LIUserCrawler()
            _user: User = parser.get_user(user_id=user_id)
            my_redis.save_cache_user(user=_user)
        except ApplicationError as e:
            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content=jsonable_encoder({'error': type(e)})
            )
    return JSONResponse(
        content=jsonable_encoder({'data': _user})
    )


@app.get('/company', description='Get company info')
async def get(company_id: str):
    _company = my_redis.get_cache_company(company_id=company_id)
    if _company is None:
        try:
            parser = LICompanyCrawler()
            _company: Company = parser.get_company(company_id=company_id)
            my_redis.save_cache_company(company=_company)
        except ApplicationError as e:
            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content=jsonable_encoder({'error': type(e)})
            )
    return JSONResponse(
        content=jsonable_encoder({'data': _company})
    )


@app.get('/posts', description='Get company\'s posts')
async def get(company_id: str):
    _posts = my_redis.get_cache_posts(company_id=company_id)
    if _posts is None or len(_posts) == 0:
        try:
            parser = LIPostCrawler()
            _posts: List[Post] = parser.get_posts(company_id=company_id)
            my_redis.save_cache_posts(posts=_posts, company_id=company_id)
        except ApplicationError as e:
            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content=jsonable_encoder({'error': type(e)})
            )

    return JSONResponse(
        content=jsonable_encoder({'data': _posts})
    )

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8080, workers=4)
