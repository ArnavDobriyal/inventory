from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    authorization_level: str
