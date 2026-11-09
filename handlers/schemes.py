from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserSchema(BaseModel):
    username: str
    password: str


class AddUserSchema(BaseModel):
    username: str
    is_active: bool
    is_admin: bool
    balance: float
    password: str


class UserAdminSchema(BaseModel):
    username: str | None = None
    is_active: bool | None = None
    is_admin: bool | None = None
    balance: float | None = None
    # password: str Надо админу право устанавливать пароль пользователя?


class UserSelfSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    is_active: bool
    is_admin: bool
    balance: float