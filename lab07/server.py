import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
BUFFER_SIZE = 1024

CHOICES = ["rock", "paper", "scissors"]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

players = {}
choices = {}
scores = {1: 0, 2: 0}


def determine_winner(choice1, choice2):
    if choice1 == choice2:
        return 0
    elif (choice1 == "rock" and choice2 == "scissors") or \
            (choice1 == "scissors" and choice2 == "paper") or \
            (choice1 == "paper" and choice2 == "rock"):
        return 1
    else:
        return 2


print("Server is running...")

while True:
    data, addr = server_socket.recvfrom(BUFFER_SIZE)
    message = data.decode()

    if addr not in players:
        if len(players) < 2:
            players[addr] = len(players) + 1
        else:
            continue

    player_id = players[addr]
    print(f"Player {player_id} chose: {message}")
    print(players)
    print(list(players.keys())[0])

    if message == "end":
        if len(players) == 2:
            other_player_addr = list(players.keys())[1] if player_id == 1 else list(players.keys())[0]
            server_socket.sendto("end".encode(), other_player_addr)
        players = {}
        choices = {}
        scores = {1: 0, 2: 0}
        print("Game ended. Waiting for new players...")
        continue

    choices[player_id] = message

    if len(choices) == 2:
        choice1 = choices[1]
        choice2 = choices[2]
        winner = determine_winner(choice1, choice2)
        if winner == 1:
            scores[1] += 1
            result1 = f"You won! Player 2 chose {choice2}. Score: {scores[1]}-{scores[2]}"
            result2 = f"You lost! Player 1 chose {choice1}. Score: {scores[1]}-{scores[2]}"
        elif winner == 2:
            scores[2] += 1
            result1 = f"You lost! Player 2 chose {choice2}. Score: {scores[1]}-{scores[2]}"
            result2 = f"You won! Player 1 chose {choice1}. Score: {scores[1]}-{scores[2]}"
        else:
            result1 = result2 = f"It's a tie! Both chose {choice1}. Score: {scores[1]}-{scores[2]}"

        server_socket.sendto(result1.encode(), list(players.keys())[0])
        server_socket.sendto(result2.encode(), list(players.keys())[1])
        choices = {}
        print(f"Round result: {result1}")
