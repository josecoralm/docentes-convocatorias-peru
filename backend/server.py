import socket
import sys
import os
import uvicorn

# Añadir directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main import app

import socket
import sys
import os
import threading
import uvicorn

# Añadir directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main import app

def create_dual_socket(port: int):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        # IPV6_V6ONLY = 0 permite aceptar tanto IPv4 (127.0.0.1) como IPv6 (localhost / ::1) en macOS
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
    except Exception as e:
        print(f"Warning IPV6_V6ONLY: {e}")
    sock.bind(("::", port))
    sock.listen(128)
    return sock

def serve_on_port(port: int):
    sock = create_dual_socket(port)
    config = uvicorn.Config(app, fd=sock.fileno(), log_level="info")
    server = uvicorn.Server(config)
    server.run()

def main():
    print("============================================================")
    print(" Servidor Activo en múltiples puertos (IPv4 + IPv6):")
    print(" - http://localhost:8000  /  http://127.0.0.1:8000")
    print(" - http://localhost:3000  /  http://127.0.0.1:3000")
    print("============================================================")
    
    # Iniciar servidor secundario en puerto 3000 en segundo plano
    t3000 = threading.Thread(target=serve_on_port, args=(3000,))
    t3000.daemon = True
    t3000.start()
    
    # Servidor principal en puerto 8000
    serve_on_port(8000)

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
