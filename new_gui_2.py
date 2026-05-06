# hybrid_gui.py

from hybrid_chat import *
from hybrid_file import *
from networking import PeerNetwork
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext


class HybridGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hybrid Encryption System")
        self.root.geometry("1000x700")

        # =========================
        # NETWORK INSTANCE (FIXED)
        # =========================
        self.net = PeerNetwork()
        self.net.start_server()
        self.on_message = self.receive_message

        # =========================
        # DARK MODE
        # =========================
        style = ttk.Style()
        style.theme_use("clam")

        bg = "#1e1e1e"
        fg = "#ffffff"
        entry_bg = "#2d2d2d"

        self.root.configure(bg=bg)

        style.configure(".", background=bg, foreground=fg)
        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=fg)
        style.configure("TButton", background=entry_bg, foreground=fg)
        style.configure("TEntry", fieldbackground=entry_bg, foreground=fg)
        style.configure("TNotebook", background=bg)
        style.configure("TNotebook.Tab", background=entry_bg, foreground=fg)

        # =========================
        # NOTEBOOK
        # =========================
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.chat_page = ttk.Frame(self.notebook)
        self.file_page = ttk.Frame(self.notebook)
        self.network_page = ttk.Frame(self.notebook)

        self.notebook.add(self.chat_page, text="Chat")
        self.notebook.add(self.file_page, text="File Transfer")
        self.notebook.add(self.network_page, text="Keys & Networking")

        self.build_chat_page()
        self.build_file_page()
        self.build_network_page()

    # =========================
    # CHAT PAGE
    # =========================
    def build_chat_page(self):
        frame = self.chat_page

        ttk.Label(frame, text="Message History").pack(anchor="w", padx=10)

        self.chat_history = scrolledtext.ScrolledText(
            frame, height=20, bg="#2d2d2d", fg="white", insertbackground="white"
        )
        self.chat_history.pack(fill="both", expand=True, padx=10, pady=5)

        input_frame = ttk.Frame(frame)
        input_frame.pack(fill="x", padx=10)

        self.message_entry = ttk.Entry(input_frame)
        self.message_entry.pack(side="left", fill="x", expand=True)

        ttk.Button(input_frame, text="Send", command=self.send_message).pack(side="left", padx=5)

        self.chat_log = scrolledtext.ScrolledText(
            frame, height=6, bg="#2d2d2d", fg="white", insertbackground="white"
        )
        self.chat_log.pack(fill="x", padx=10, pady=5)

    def send_message(self):
        message = self.message_entry.get()

        if not message:
            return

        self.chat_history.insert(tk.END, f"You: {message}\n")

        enc_msg, msg_key = hb_encrypt(message)

        ip = self.ip_entry.get()

        if not ip:
            self.chat_log.insert(tk.END, "No IP set.\n")
            return

        self.net.send_message(ip, enc_msg, msg_key)

        self.message_entry.delete(0, tk.END)

    # =========================
    # FILE PAGE
    # =========================
    def build_file_page(self):
        frame = self.file_page

        ttk.Label(frame, text="File Path").pack(anchor="w", padx=10)

        path_frame = ttk.Frame(frame)
        path_frame.pack(fill="x", padx=10)

        self.file_path = ttk.Entry(path_frame)
        self.file_path.pack(side="left", fill="x", expand=True)

        ttk.Button(path_frame, text="Browse", command=self.choose_file).pack(side="left", padx=5)
        ttk.Button(path_frame, text="Send File", command=self.send_file).pack(side="left")

        self.file_history = scrolledtext.ScrolledText(frame, height=25)
        self.file_history.pack(fill="both", expand=True, padx=10, pady=5)

    def choose_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.file_path.delete(0, tk.END)
            self.file_path.insert(0, path)

    def send_file(self):
        path = self.file_path.get()
        ip = self.ip_entry.get()

        if not path or not ip:
            self.file_history.insert(tk.END, "Missing file or IP.\n")
            return

        try:
            file_enc, file_key = encrypt_file(path)

            self.net.send_file(ip, file_enc, file_key)

            self.file_history.insert(tk.END, f"Sent: {path}\n")

        except Exception as e:
            self.file_history.insert(tk.END, f"Error: {e}\n")
    
    def receive_message(self, sender, message):
    # Tkinter-safe update (important because networking runs in another thread)
        self.root.after(0, self._display_message, sender, message)
    def _display_message(self, sender, message):
        self.chat_history.insert(
            tk.END,
            f"{sender}: {message}\n"
        )

        self.chat_history.see(tk.END)

        self.chat_log.insert(
            tk.END,
            "Message received\n"
        )

        self.chat_log.see(tk.END)

    # =========================
    # NETWORK PAGE
    # =========================
    def build_network_page(self):
        frame = self.network_page

        ttk.Label(frame, text="IP Address").pack(anchor="w", padx=10)
        self.ip_entry = ttk.Entry(frame)
        self.ip_entry.pack(fill="x", padx=10)

        ttk.Label(frame, text="Port").pack(anchor="w", padx=10)
        self.port_entry = ttk.Entry(frame)
        self.port_entry.pack(fill="x", padx=10)

        ttk.Button(frame, text="Connect", command=self.connect_network).pack(pady=5)
        ttk.Button(frame, text="Reconnect", command=self.reconnect).pack(pady=5)
        ttk.Button(frame, text="Load Keys", command=self.load_keys).pack(pady=5)

        self.public_key_box = scrolledtext.ScrolledText(frame, height=6)
        self.public_key_box.pack(fill="x", padx=10)

        self.private_key_box = scrolledtext.ScrolledText(frame, height=6)
        self.private_key_box.pack(fill="x", padx=10)

        self.network_log = scrolledtext.ScrolledText(frame, height=8)
        self.network_log.pack(fill="both", expand=True, padx=10)

    def connect_network(self):
        ip = self.ip_entry.get()
        port = self.port_entry.get()

        self.network_log.insert(tk.END, f"Connecting to {ip}:{port}\n")

    def reconnect(self):
        self.network_log.insert(tk.END, "Reconnecting...\n")

    def load_keys(self):
        try:
            with open("public.pem", "r") as f:
                pub = f.read()

            with open("private.pem", "r") as f:
                priv = f.read()

            self.public_key_box.delete("1.0", tk.END)
            self.private_key_box.delete("1.0", tk.END)

            self.public_key_box.insert(tk.END, pub)
            self.private_key_box.insert(tk.END, priv)

        except Exception as e:
            self.network_log.insert(tk.END, f"Key load error: {e}\n")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = HybridGUI(root)
    root.mainloop()