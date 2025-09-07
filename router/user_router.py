from controllers.user_controller import UserController
from server.http_response import HttpResponse

def routes(method, path, query_params=None, body=None):
    if path == '/users' and method == 'GET':
        return HttpResponse.build(200, UserController.list_users(query_params))

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

    elif path == '/users' and method == 'POST':
        user = UserController.create_user(body)
        return HttpResponse.build(201, user)

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

    elif path.startswith('/users/') and method == 'DELETE':
        try:
            user_id = int(path.split('/')[-1])
        except ValueError:
            return HttpResponse.build(400, {"error": "Invalid user ID"})
        success = UserController.delete_user(user_id)
        if success:
            return HttpResponse.build(204, {"success": True})
        else:
            return HttpResponse.build(404, {"error": "User not found"})

    else:
        return None  # Let main router handle unknown routes
