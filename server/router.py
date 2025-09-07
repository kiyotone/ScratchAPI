from controllers.user_controller import UserController
from server.http_response import HttpResponse

class Router:
    @staticmethod
    def route(method, path, query_params=None, body=None):
        # GET all users
        if path == '/users' and method == 'GET':
            users = UserController.list_users(query_params)
            return HttpResponse.build(200, users)

        # GET a single user by ID
        elif path.startswith('/users/') and method == 'GET':
            try:
                user_id = int(path.split('/')[-1])
            except ValueError:
                return HttpResponse.build(400, {"error": "Invalid user ID"})
            user = UserController.get_user(user_id)
            if user:
                return HttpResponse.build(200, user)
            else:
                return HttpResponse.build(404, {"error": "User not found"})

        # CREATE a new user
        elif path == '/users' and method == 'POST':
            user = UserController.create_user(body)
            return HttpResponse.build(201, user)

        # UPDATE a user by ID
        elif path.startswith('/users/') and method == 'PUT':
            try:
                user_id = int(path.split('/')[-1])
            except ValueError:
                return HttpResponse.build(400, {"error": "Invalid user ID"})
            updated_user = UserController.update_user(user_id, body)
            if updated_user:
                return HttpResponse.build(200, updated_user)
            else:
                return HttpResponse.build(404, {"error": "User not found"})

        # DELETE a user by ID
        elif path.startswith('/users/') and method == 'DELETE':
            try:
                user_id = int(path.split('/')[-1])
            except ValueError:
                return HttpResponse.build(400, {"error": "Invalid user ID"})
            success = UserController.delete_user(user_id)
            if success:
                return HttpResponse.build(204, None)
            else:
                return HttpResponse.build(404, {"error": "User not found"})

        # Endpoint not found
        else:
            return HttpResponse.build(404, {"error": "Endpoint not found"})
