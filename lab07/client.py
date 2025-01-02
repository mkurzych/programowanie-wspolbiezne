import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
BUFFER_SIZE = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

print("Client is running...")

while True:
    choice = input("Enter your choice (rock, paper, scissors) or 'end' to quit: ").lower()
    if choice not in ["rock", "paper", "scissors", "end"]:
        print("Invalid choice. Please try again.")
        continue

    client_socket.sendto(choice.encode(), (SERVER_IP, SERVER_PORT))

    if choice == "end":
        break

    response, _ = client_socket.recvfrom(BUFFER_SIZE)
    response_message = response.decode()
    print(response_message)

    if response_message == "end":
        break

client_socket.close()
exit()