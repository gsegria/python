import socket
import threading

HOST = '0.0.0.0'
PORT = 65432

clients = []  # 保存所有連線 client

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    clients.append(conn)
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode()
            print(f"Received from {addr}: {msg}")

            # 廣播給其他 client
            for c in clients[:]:
                if c != conn:
                    try:
                        c.sendall(f"[{addr}] {msg}".encode())
                    except:
                        clients.remove(c)
                        c.close()
    except Exception as e:
        print(f"Error with {addr}: {e}")
    finally:
        print(f"Disconnected {addr}")
        if conn in clients:
            clients.remove(conn)
        conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()
