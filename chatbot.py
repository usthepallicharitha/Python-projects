import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("✅ Server started... Waiting for clients")

    clients = []

    def broadcast(message, sender):
        for client in clients:
            if client != sender:
                client.send(message)

    def handle_client(client):
        while True:
            try:
                message = client.recv(1024)
                broadcast(message, client)
            except:
                clients.remove(client)
                client.close()
                break

    while True:
        client, addr = server.accept()
        print(f"🔗 Connected: {addr}")
        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    name = input("Enter your name: ")
    print("🟢 Connected to chat")

    def receive():
        while True:
            try:
                msg = client.recv(1024).decode()
                print(msg)
            except:
                print("❌ Disconnected")
                client.close()
                break

    def send():
        while True:
            message = input()
            client.send(f"{name}: {message}".encode())

    threading.Thread(target=receive).start()
    threading.Thread(target=send).start()

print("1. Start Server")
print("2. Start Client")
choice = input("Enter choice: ")

if choice == '1':
    start_server()
elif choice == '2':
    start_client()
else:
    print("Invalid choice")
