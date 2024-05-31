from pydantic import BaseModel


class UnknownError(BaseModel):
    code: int = 42  # универсальный ответ
    message: str = "Unknown error"


class BadBeerError(UnknownError):
    code: int = 9  # Балтика
    message: str = "Bad beer"


class BadCityError(UnknownError):
    code: int = 55  # регион Омска
    message: str = "Bad city"


class BadManufacturerError(UnknownError):
    code: int = 69  # nice.
    message: str = "Bad manufacturer"


class BadUserError(UnknownError):
    code: int = 11  # модель Скиппи из киберпанка
    message: str = "Bad user"


class BadReviewError(UnknownError):
    code: int = 15  # оценка 1/5
    message: str = "Bad review"
