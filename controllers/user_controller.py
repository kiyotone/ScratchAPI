from models.user import User


class UserController:
    @staticmethod
    def list_users(query_params=None):
        """
        Get all users. If query_params are provided, filter by them.
        Example: /users?name=John
        """
        if query_params:
            # convert query_params (list values) to single values
            flat_params = {k: v[0] if isinstance(v, list) else v for k, v in query_params.items()}
            users = User.filter(**flat_params)
        else:
            users = User.all()

        return [u.to_dict() for u in users]

    @staticmethod
    def get_user(user_id: int):
        """
        Get single user by ID
        """
        user = User.get(id=user_id)
        return user.to_dict() if user else None

    @staticmethod
    def create_user(data: dict):
        """
        Create a new user
        """
        user = User.create(**data)
        return user.to_dict()

    @staticmethod
    def update_user(user_id: int, data: dict):
        """
        Update a user by ID
        """
        success = User.update(user_id, **data)
        if not success:
            return None
        updated_user = User.get(id=user_id)
        return updated_user.to_dict() if updated_user else None

    @staticmethod
    def delete_user(user_id: int):
        """
        Delete a user by ID
        """
        success = User.delete(user_id)
        return success
