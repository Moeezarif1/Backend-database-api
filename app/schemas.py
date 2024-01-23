from pydantic import BaseModel


class Credentials(BaseModel):
    dbname: str
    user: str
    password: str
    host: str
    port: int
