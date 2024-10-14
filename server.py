import socket

def gacha_server():
    # Create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the port
    server.bind(("localhost", 19797))  # Localhost with the specified port
    server.listen(5)
    print("Gacha server is running... Waiting for connections.")

    while True:  # Loop to continuously accept clients
        client_socket, addr = server.accept()
        print(f"Client connected from {addr}")

        # Admin selects a reward for the client
        rewards = ["CASHBACK 2X!", "CASHBACK 1X!", "ZONK", "CASHBACK 3X!", "CASHBACK 0.5X!"]
        print("Available rewards:")
        for i, reward in enumerate(rewards, 1):
            print(f"{i}. {reward}")

        # Receive input from admin: can be a number or a name of the reward
        choice = input("Select a reward for the client (enter number or name): ").strip()

        # Validate input: check if it's a number or a valid reward name
        if choice.isdigit():  # If input is a number
            index = int(choice) - 1
            if 0 <= index < len(rewards):
                selected_reward = rewards[index]
            else:
                print("Invalid number! Defaulting to 'ZONK'.")
                selected_reward = "ZONK"
        else:  # If input is a reward name
            if choice in rewards:
                selected_reward = choice
            else:
                print("Invalid reward name! Defaulting to 'ZONK'.")
                selected_reward = "ZONK"

        # Send the selected reward to the client
        client_socket.send(selected_reward.encode())
        print(f"Sent {selected_reward} to the client.")
        
        # Close the client socket after sending the reward
        client_socket.close()
        print("Waiting for the next client...\n")

if __name__ == "__main__":
    gacha_server()
