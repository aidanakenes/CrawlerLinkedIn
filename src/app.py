import uvicorn
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.models.user import User
from src.models.company import Company
from src.service.crawler_user import LIUserCrawler
from src.service.crawler_company import LICompanyCrawler
from src.utils.err_utils import ApplicationError

app = FastAPI()


@app.get('/profile', description='Get profile info')
async def get(username: str):
    try:
        parser = LIUserCrawler()
        _user: User = parser.get_user(username=username)
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


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8080, workers=4)
