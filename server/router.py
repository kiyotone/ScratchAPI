from router import user_router  # import all routers here
from server.http_response import HttpResponse

ROUTERS = [user_router.routes]  # you can add more routers like product_router.routes

class Router:
    @staticmethod
    def route(method, path, query_params=None, body=None):
        for r in ROUTERS:
            response = r(method, path, query_params, body)
            if response:
                return response
        return HttpResponse.build(404, {"error": "Endpoint not found"})
