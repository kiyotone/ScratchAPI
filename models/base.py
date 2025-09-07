from database.manager import DatabaseManager


class BaseModel:
    db = DatabaseManager("app.db")   # shared DB instance
    table_name: str = None           # must be overridden
    fields: dict = {}                # must be overridden

    def __init__(self, **kwargs):
        for field, field_type in self.fields.items():
            value = kwargs.get(field, None)
            if value is not None and not isinstance(value, field_type):
                raise TypeError(f"{field} must be {field_type.__name__}, got {type(value).__name__}")
            setattr(self, field, value)

    def to_dict(self):
        return {field: getattr(self, field, None) for field in self.fields}

    # ---------- Class-level ORM-like methods ----------
    @classmethod
    def create_table(cls):
        cls.db.create_table(cls.table_name or cls.__name__.lower(), cls.fields)

    @classmethod
    def create(cls, **kwargs):
        record_id = cls.db.insert(cls.table_name, kwargs)
        return cls.get(id=record_id)

    @classmethod
    def all(cls):
        rows = cls.db.get_all(cls.table_name)
        return [cls(**row) for row in rows]

    @classmethod
    def get(cls, **kwargs):
        if "id" in kwargs:
            row = cls.db.get_by_id(cls.table_name, kwargs["id"])
            if row:
                return cls(**row)
        return None

    @classmethod
    def filter(cls, **kwargs):
        if not kwargs:
            return cls.all()
        conditions = " AND ".join([f"{k}=?" for k in kwargs.keys()])
        sql = f"SELECT * FROM {cls.table_name} WHERE {conditions}"
        rows = cls.db.execute_raw(sql, tuple(kwargs.values()))
        return [cls(**row) for row in rows]

    @classmethod
    def update(cls, record_id, **kwargs):
        updated = cls.db.update(cls.table_name, record_id, kwargs)
        return updated > 0

    @classmethod
    def delete(cls, record_id):
        deleted = cls.db.delete(cls.table_name, record_id)
        return deleted > 0

    # ---------- Instance-level ----------
    def save(self):
        data = self.to_dict()
        if getattr(self, "id", None):
            self.update(self.id, **data)
        else:
            new = self.create(**data)
            self.id = new.id
        return self

    def delete_instance(self):
        if getattr(self, "id", None):
            return self.delete(self.id)
        return False
