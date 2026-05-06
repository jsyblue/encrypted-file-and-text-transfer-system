import socket
import threading
import pickle
from hybrid_chat import hb_decryption


class PeerNetwork:
    def __init__(self, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Start listening for incoming encrypted messages
    def start_server(self):
        self.server.bind((self.host, self.port))
        self.server.listen()

        print(f"Listening on {self.host}:{self.port}")

        threading.Thread(target=self.listen_for_messages, daemon=True).start()

    def listen_for_messages(self):
        while True:
            conn, addr = self.server.accept()

            try:
                data = conn.recv(65536)

                if data:
                    encrypted_message, encrypted_key = pickle.loads(data)

                    decrypted = hb_decryption(
                        encrypted_message,
                        encrypted_key
                    )

                    print(f"\nMessage from {addr[0]}: {decrypted}")

            except Exception as e:
                print("Receive error:", e)

            finally:
                conn.close()

    # Send encrypted packet
    def send_message(self, target_ip, encrypted_message, encrypted_key):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client.connect((target_ip, self.port))

            packet = pickle.dumps(
                (encrypted_message, encrypted_key)
            )

            client.sendall(packet)

            print("Message sent")

        except Exception as e:
            print("Send error:", e)

        finally:
            client.close()


    def send_file(self,ip, encrypted_file, encrypted_key):
        """
        Sends encrypted file to peer
        """

        port = 5000

        data = {
            "type": "file",
            "file": encrypted_file,
            "key": encrypted_key
        }

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))

        client.sendall(pickle.dumps(data))

        client.close()