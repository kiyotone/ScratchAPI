import socket
import threading
from server.client_thread import client_thread
from utils.logger import setup_logger



logger = setup_logger()

HOST = '127.0.0.1'
PORT = 8080

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        logger.info(f"Server running at http://{HOST}:{PORT}")

        while True:
            conn_sock, addr = s.accept()
            threading.Thread(target=client_thread, args=(conn_sock,)).start()

if __name__ == "__main__":
    run_server()
    

