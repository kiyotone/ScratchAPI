from .base import BaseModel

class User(BaseModel):
    table_name = "users"
    fields = {
        "id": {"type": int},
        "name": {"type": str, "required": True},
        "email": {"type": str, "required": True, "unique": True},
        "role": {"type": str, "required": True, "validator": lambda v: v in ["Admin", "Member"]}
    }
