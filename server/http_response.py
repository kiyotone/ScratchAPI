import json

class HttpResponse:
    REASONS = {
        200: 'OK',
        201: 'Created',
        400: 'Bad Request',
        404: 'Not Found',
        500: 'Internal Server Error'
    }

    @staticmethod
    def build(status_code, body_dict):
        body = json.dumps(body_dict)
        response = f"HTTP/1.1 {status_code} {HttpResponse.REASONS.get(status_code, '')}\r\n"
        response += "Content-Type: application/json\r\n"
        response += f"Content-Length: {len(body.encode())}\r\n"
        response += "Connection: close\r\n\r\n"
        response += body
        return response
