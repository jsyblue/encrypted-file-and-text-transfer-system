import os
import threading
import queue

from hybrid_chat import hb_encrypt
from hybrid_file import encrypt_file
from networking import PeerNetwork


class HybridCLI:
    def __init__(self):
        self.net = PeerNetwork()
        self.net.start_server()

        self.ip = None
        self.port = 5000

        self.message_queue = queue.Queue()
        self.running = True

        # Hook receiver callback
        self.on_message = self.receive_message

    # =========================
    # RECEIVE CALLBACK
    # =========================
    def receive_message(self, sender, message):
        self.message_queue.put((sender, message))

    # =========================
    # MENU
    # =========================
    def menu(self):
        while self.running:
            print("\n============================")
            print(" HYBRID ENCRYPTION CLI")
            print("============================")
            print("1. Set Target IP")
            print("2. Send Message")
            print("3. Send File")
            print("4. Show Keys")
            print("5. Listener")
            print("6. Exit")

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
                self.listener_mode()

            elif choice == "6":
                self.exit_program()

            else:
                print("Invalid option")

    # =========================
    # SET TARGET
    # =========================
    def set_ip(self):
        self.ip = input("Enter target IP: ")
        self.port = int(input("Enter port (default 5000): ") or 5000)

        self.net.port = self.port

        print(f"[+] Target set: {self.ip}:{self.port}")

    # =========================
    # SEND MESSAGE
    # =========================
    def send_message(self):
        if not self.ip:
            print("[-] Set target IP first")
            return

        msg = input("Message: ")

        enc_msg, enc_key = hb_encrypt(msg)

        self.net.send_message(
            self.ip,
            enc_msg,
            enc_key
        )

        print("[+] Message sent")

    # =========================
    # SEND FILE
    # =========================
    def send_file(self):
        if not self.ip:
            print("[-] Set target IP first")
            return

        path = input("File path: ")

        if not os.path.exists(path):
            print("[-] File not found")
            return

        try:
            enc_file, enc_key = encrypt_file(path)

            self.net.send_file(
                self.ip,
                enc_file,
                enc_key
            )

            print("[+] File sent")

        except Exception as e:
            print("Error:", e)

    # =========================
    # LISTENER MODE
    # =========================
    def listener_mode(self):
        print("\n=== LISTENER MODE ===")
        print("Waiting for messages...")
        print("Press q to return\n")

        while True:
            while not self.message_queue.empty():
                sender, msg = self.message_queue.get()
                print(f"\n[{sender}] {msg}")

            cmd = input()

            if cmd.lower() == "q":
                break

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
    # EXIT
    # =========================
    def exit_program(self):
        print("Shutting down...")
        self.running = False

    # =========================
    # RUN
    # =========================
    def run(self):
        print("Hybrid Encryption CLI")
        print(f"Listening on port {self.port}")
        self.menu()


if __name__ == "__main__":
    app = HybridCLI()
    app.run()