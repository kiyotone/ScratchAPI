import threading
from server.request_handler import RequestHandler
from utils.logger import setup_logger

logger = setup_logger()

def client_thread(conn_sock):
    try:
        request = conn_sock.recv(4096).decode()
        if request:
            logger.info(f"Received request: {request.splitlines()[0]}")
            response = RequestHandler.handle(request)
            conn_sock.sendall(response.encode())
    finally:
        conn_sock.close()
