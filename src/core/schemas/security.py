from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    first_name: str
    last_name: str
    sub: str
    link: str
