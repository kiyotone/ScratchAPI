from .base import BaseModel

class User(BaseModel):
    table_name = "users"
    fields = {
        "id": int,
        "name": str,
        "email": str,
        "role": str
    }
