import json
from urllib.parse import urlparse, parse_qs
from server.router import Router
from server.http_response import HttpResponse
from utils.logger import setup_logger

logger = setup_logger()

class RequestHandler:
    @staticmethod
    def handle(request_text):
        try:
            lines = request_text.split('\r\n')
            method, path, _ = lines[0].split()
            
            # Headers
            headers = {}
            i = 1
            while lines[i]:
                key, value = lines[i].split(': ', 1)
                headers[key] = value
                i += 1
            body = '\r\n'.join(lines[i+1:])

            parsed_url = urlparse(path)
            path = parsed_url.path
            query_params = parse_qs(parsed_url.query)

            body_data = json.loads(body) if body else {}

            return Router.route(method, path, query_params, body_data)

        except Exception as e:
            logger.exception("Error processing request")
            return HttpResponse.build(500, {"error": str(e)})
