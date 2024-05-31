from fastapi import FastAPI, HTTPException, Response
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise

from core.settings import TORTOISE_ORM
from v1.endpoints.beer import beer_router
from v1.endpoints.city import city_router
from v1.endpoints.user import user_router
from v1.endpoints.reviews import review_router
from v1.endpoints.manufacturers import manufacturer_router

tags = [
    {
        "name": "Beer",
        "description": "Подпивасный CRUD"
    },
    {
        "name": "City",
        "description": "Подпивасно-городской CRUD"
    },
    {
        "name": "Manufacturer",
        "description": "Подпивасно-производительский CRUD"
    },
    {
        "name": "User",
        "description": "Подпивасно-юзерский CRUD"
    }
]

app = FastAPI(docs_url=None, redoc_url=None, openapi_tags=tags)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
            swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.exception_handler(HTTPException)
async def show_error(response: Response, exc: HTTPException):
    response.status_code = exc.status_code
    assert issubclass(exc.detail, BaseModel)  # type: ignore
    return ORJSONResponse(status_code=exc.status_code,
                          content=exc.detail().dict())


app.include_router(beer_router)
app.include_router(city_router)
app.include_router(manufacturer_router)
app.include_router(user_router)
app.include_router(review_router)
register_tortoise(app, config=TORTOISE_ORM)
