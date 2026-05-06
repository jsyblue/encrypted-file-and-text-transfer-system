# Hybrid Encryption CLI Test Environment
# Linux-friendly terminal version for presentation testing

import socket
import threading
import pickle
import os

from hybrid_chat import hb_encrypt, hb_decryption
from hybrid_file import encrypt_file
from networking import PeerNetwork


class HybridCLI:
    def __init__(self):
        self.net = PeerNetwork()
        self.net.start_server()

        self.ip = None
        self.port = 5000

    # =========================
    # MENU
    # =========================
    def menu(self):
        while True:
            print("\n============================")
            print(" HYBRID ENCRYPTION CLI")
            print("============================")
            print("1. Set Target IP")
            print("2. Send Message")
            print("3. Send File")
            print("4. Show Keys")
            print("5. Exit")

            choice = input("Select option: ")

            if choice == "1":
                self.set_ip()
            elif choice == "2":
                self.send_message()
            elif choice == "3":
                self.send_file()
            elif choice == "4":
                self.show_keys()
            elif choice == "5":
                break
            else:
                print("Invalid option")

    # =========================
    # SET IP
    # =========================
    def set_ip(self):
        self.ip = input("Enter target IP: ")
        self.port = int(input("Enter port (default 5000): ") or 5000)

        print(f"[+] Target set to {self.ip}:{self.port}")

    # =========================
    # SEND MESSAGE
    # =========================
    def send_message(self):
        if not self.ip:
            print("[-] Set IP first")
            return

        message = input("Message: ")

        enc_msg, msg_key = hb_encrypt(message)

        self.net.send_message(
            self.ip,
            enc_msg,
            msg_key
        )

        print("[+] Message sent")

    # =========================
    # SEND FILE
    # =========================
    def send_file(self):
        if not self.ip:
            print("[-] Set IP first")
            return

        path = input("File path: ")

        if not os.path.exists(path):
            print("[-] File not found")
            return

        try:
            file_enc, file_key = encrypt_file(path)

            self.net.send_file(
                self.ip,
                file_enc,
                file_key
            )

            print("[+] File sent")

        except Exception as e:
            print(f"[-] Error: {e}")

    # =========================
    # SHOW KEYS
    # =========================
    def show_keys(self):
        try:
            with open("public.pem", "r") as f:
                print("\n--- PUBLIC KEY ---")
                print(f.read())

            with open("private.pem", "r") as f:
                print("\n--- PRIVATE KEY ---")
                print(f.read())

        except FileNotFoundError:
            print("[-] Keys not found")

    # =========================
    # RUN CLI
    # =========================
    def run(self):
        print("Starting Hybrid CLI...")
        print("Server listening on port 5000")
        self.menu()


if __name__ == "__main__":
    app = HybridCLI()
    app.run()