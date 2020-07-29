import uvicorn

from fastapi import FastAPI, Request, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.models.user import User
from src.models.company import Company
from src.service.crawler import LICrawler

app = FastAPI()


@app.get('/profile', description='Get profile info')
async def get(user_url: str):
    parser = LICrawler()
    _user: User = parser.get_user(user_link=user_url)
    return JSONResponse(
        content=jsonable_encoder({'data': _user})
    )


@app.get('/company', description='Get company info')
async def get(company_link: str):
    parser = LICrawler()
    _company: Company = parser.get_company(user_link=company_link)
    return JSONResponse(
        content=jsonable_encoder({'data': _company})
    )


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8080, workers=4)
