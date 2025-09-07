from database.manager import DatabaseManager

class BaseModel:
    db = DatabaseManager("app.db")
    table_name: str = None
    fields: dict = {}
    
    # Track which tables have been created to avoid redundant calls
    _created_tables = set()

    def __init__(self, **kwargs):
        """
        Instantiate object from data (DB row or input dictionary)
        """
        for field_name, meta in self.fields.items():
            value = kwargs.get(field_name, meta.get("default"))
            setattr(self, field_name, value)

    def to_dict(self):
        return {field: getattr(self, field, None) for field in self.fields}

    # ---------- Validation ----------
    @classmethod
    def _validate_fields(cls, data, updating=False, record_id=None):
        for field_name, meta in cls.fields.items():
            value = data.get(field_name, meta.get("default"))
            field_type = meta.get("type")
            required = meta.get("required", False)
            validator = meta.get("validator")
            unique = meta.get("unique", False)

            # Required check
            if required and value is None:
                raise ValueError(f"Field '{field_name}' is required")

            # Type check
            if value is not None and field_type and not isinstance(value, field_type):
                raise TypeError(f"Field '{field_name}' must be {field_type.__name__}, got {type(value).__name__}")

            # Custom validator
            if validator and value is not None and not validator(value):
                raise ValueError(f"Field '{field_name}' failed validation")

            # Unique check
            if unique and value is not None:
                existing = cls.filter(**{field_name: value})
                if existing and (not updating or existing[0].id != record_id):
                    raise ValueError(f"Field '{field_name}' must be unique, '{value}' already exists")

    # ---------- Table management ----------
    @classmethod
    def _ensure_table(cls):
        if cls.table_name not in cls._created_tables:
            cls.db.create_table(cls.table_name or cls.__name__.lower(), cls.fields)
            cls._created_tables.add(cls.table_name)

    # ---------- Class-level ORM-like methods ----------
    @classmethod
    def all(cls):
        cls._ensure_table()
        rows = cls.db.get_all(cls.table_name)
        return [cls(**row) for row in rows]

    @classmethod
    def get(cls, **kwargs):
        cls._ensure_table()
        if "id" in kwargs:
            row = cls.db.get_by_id(cls.table_name, kwargs["id"])
            if row:
                return cls(**row)
        return None

    @classmethod
    def filter(cls, **kwargs):
        cls._ensure_table()
        if not kwargs:
            return cls.all()
        conditions = " AND ".join([f"{k}=?" for k in kwargs.keys()])
        sql = f"SELECT * FROM {cls.table_name} WHERE {conditions}"
        rows = cls.db.execute_raw(sql, tuple(kwargs.values()))
        return [cls(**row) for row in rows]

    @classmethod
    def create(cls, **kwargs):
        cls._ensure_table()
        cls._validate_fields(kwargs)
        record_id = cls.db.insert(cls.table_name, kwargs)
        return cls.get(id=record_id)

    @classmethod
    def update(cls, record_id, **kwargs):
        cls._ensure_table()
        cls._validate_fields(kwargs, updating=True, record_id=record_id)
        updated = cls.db.update(cls.table_name, record_id, kwargs)
        return updated > 0

    @classmethod
    def delete(cls, record_id):
        cls._ensure_table()
        deleted = cls.db.delete(cls.table_name, record_id)
        return deleted > 0
