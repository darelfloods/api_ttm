from pydantic import BaseModel

from . import UserSchema
from . import TokenSchema


class Authentication(BaseModel):
    token: TokenSchema.Token
    user: UserSchema.Read
    