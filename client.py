import socket
import time
import random
import threading
from colorama import Fore, Style, init
import pyfiglet

# Initialize colorama
init(autoreset=True)

def display_fake_spin(rewards):
    """Fungsi untuk menampilkan daftar hadiah yang berganti-ganti seolah-olah sedang diacak"""
    while not stop_spin.is_set():
        selected_reward = random.choice(rewards)
        print(Fore.YELLOW + f"Spinning... Current selection: {selected_reward}", end='\r')
        time.sleep(0.1)  # Waktu delay cepat (0.1 detik)

def gacha_client():
    rewards = ["CASHBACK 1X!", "CASHBACK 2X!", "ZONK", "CASHBACK 3X!", "CASHBACK 0.5X!"]
    
    try:
        # Displaying the Gacha title with ASCII art
        print(Fore.CYAN + pyfiglet.figlet_format("Gacha Game"))
        print(Style.BRIGHT + Fore.MAGENTA + "Daftar Hadiah:")
        for i, reward in enumerate(rewards, 1):
            print(Fore.GREEN + f"{i}. {reward}")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("0.tcp.ap.ngrok.io", 16189))  # Pastikan client menggunakan port yang sama
        print(Fore.CYAN + "\nConnecting to gacha server...\n")
        
        # Meminta user untuk memasukkan command 'start' sebelum memulai gacha
        command = input(Fore.YELLOW + "Enter 'start' to begin the gacha: ")
        while command.lower() != 'start':
            command = input(Fore.RED + "Invalid command. Please enter 'start' to begin the gacha: ")

        print(Fore.CYAN + "Starting gacha...\n")

        # Thread untuk menampilkan spin palsu
        global stop_spin
        stop_spin = threading.Event()
        spin_thread = threading.Thread(target=display_fake_spin, args=(rewards,))
        spin_thread.start()

        # Terima hadiah dari server
        reward = client_socket.recv(1024).decode()

        # Hentikan spin ketika hadiah dari server diterima
        stop_spin.set()
        spin_thread.join()

        # Tampilkan hadiah yang diterima
        print(Fore.GREEN + f"\nCongratulations! You won: {reward}")

        # Keep the window open
        input(Fore.YELLOW + "\nPress Enter to close...")

    except ConnectionError:
        print(Fore.RED + "Failed to connect to the server. Please try again later.")
    finally:
        client_socket.close()  # Pastikan untuk menutup socket setelah selesai

if __name__ == "__main__":
    gacha_client()
