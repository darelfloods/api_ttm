from pydantic import BaseModel


class Base(BaseModel):
    client_phone: str
    amount: str
    firstname: str | None = None
    lastname: str
    email: str
    network: str
    rate_id: int


class Create(Base):
    pass
