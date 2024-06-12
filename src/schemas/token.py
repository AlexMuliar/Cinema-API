from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPair(BaseModel):
    access_token: Token
    refresh_token: Token


class TokenData(BaseModel):
    username: str | None = None
