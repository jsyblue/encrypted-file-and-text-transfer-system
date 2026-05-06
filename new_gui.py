# hybrid_gui.py
# GUI for Hybrid Chat + File Encryption System
# Built with Tkinter
#
# Pages:
# 1. Chat
# 2. File Transfer
# 3. Key Management & Networking
#
# Plug your backend functions where marked
from hybrid_chat import *
from hybrid_file import *
from networking import PeerNetwork as net 
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext


class HybridGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hybrid Encryption System")
        self.root.geometry("1000x700")
        # Dark Mode Styling
        style = ttk.Style()
        style.theme_use("clam")

        # Main colors
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

        style.map("TButton",
                background=[("active", "#3a3a3a")])

        style.map("TNotebook.Tab",
                background=[("selected", "#444444")])

        # -----------------------------
        # MAIN NOTEBOOK (Tabbed Pages)
        # -----------------------------
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Create pages
        self.chat_page = ttk.Frame(self.notebook)
        self.file_page = ttk.Frame(self.notebook)
        self.network_page = ttk.Frame(self.notebook)

        self.notebook.add(self.chat_page, text="Chat")
        self.notebook.add(self.file_page, text="File Transfer")
        self.notebook.add(self.network_page, text="Keys & Networking")

        # Build each page
        self.build_chat_page()
        self.build_file_page()
        self.build_network_page()

    # ==================================================
    # PAGE 1 - CHAT
    # ==================================================
    def build_chat_page(self):
        frame = self.chat_page

        # Message history box
        ttk.Label(frame, text="Message History").pack(anchor="w", padx=10)

        self.chat_history = scrolledtext.ScrolledText( frame,
    height=20,
    bg="#2d2d2d",
    fg="white",
    insertbackground="white")
        self.chat_history.pack(fill="both", expand=True, padx=10, pady=5)

        # Input frame
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill="x", padx=10)

        self.message_entry = ttk.Entry(input_frame)
        self.message_entry.pack(side="left", fill="x", expand=True)

        send_btn = ttk.Button(
            input_frame,
            text="Send",
            command=self.send_message
        )
        send_btn.pack(side="left", padx=5)

        # Log box
        ttk.Label(frame, text="Logs").pack(anchor="w", padx=10, pady=(10, 0))

        self.chat_log = scrolledtext.ScrolledText( frame,
    height=20,
    bg="#2d2d2d",
    fg="white",
    insertbackground="white")
        self.chat_log.pack(fill="x", padx=10, pady=5)

    def send_message(self):
        message = self.message_entry.get()

        if message:
            # Show in chat history
            self.chat_history.insert(tk.END, f"You: {message}\n")

            # Log event
            self.log_chat(f"Message sent: {message}")

            enc_msg, msg_key = hb_encrypt(message)
            net.send_message(ip_entry.get(),
                             enc_msg,
                             msg_key
                             )
            
            # basically whats happening:
            # encrypted = encrypt_message(message)
            # network_send(encrypted)
           

            self.message_entry.delete(0, tk.END)

    def receive_message(self, message):
        """Call this from networking code when a message arrives"""
        self.chat_history.insert(tk.END, f"Peer: {message}\n")
        self.log_chat(f"Message received")

    def log_chat(self, text):
        self.chat_log.insert(tk.END, text + "\n")
        self.chat_log.see(tk.END)

    
    # PAGE 2 - FILE TRANSFER

    def build_file_page(self):
        frame = self.file_page

        ttk.Label(frame, text="File Path").pack(anchor="w", padx=10)

        path_frame = ttk.Frame(frame)
        path_frame.pack(fill="x", padx=10, pady=5)

        self.file_path = ttk.Entry(path_frame)
        self.file_path.pack(side="left", fill="x", expand=True)

        browse_btn = ttk.Button(
            path_frame,
            text="Choose Path",
            command=self.choose_file
        )
        browse_btn.pack(side="left", padx=5)

        send_btn = ttk.Button(
            path_frame,
            text="Send File",
            command=self.send_file
        )
        send_btn.pack(side="left")

        ttk.Label(frame, text="File Transfer History").pack(anchor="w", padx=10)

        self.file_history = scrolledtext.ScrolledText(frame, height=25)
        self.file_history.pack(fill="both", expand=True, padx=10, pady=5)

    def choose_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.file_path.delete(0, tk.END)
            self.file_path.insert(0, path)

    def send_file(self):
        path = self.file_path.get()

        if path:
            self.file_history.insert(
                tk.END,
                f"Sent File: {path}\n"
            )

            
            # ---------------------------
            # PLUG FILE ENCRYPTION HERE
            
            file_enc, file_key = encrypt_file(path)
            net.send_file(self.ip_entry.get(),
                          file_enc,
                          file_key)

    def receive_file(self, filename):
        """Call this when a file is received"""
        self.file_history.insert(
            tk.END,
            f"Received File: {filename}\n"
        )

    # ==================================================
    # PAGE 3 - KEYS & NETWORKING
    # ==================================================
    def build_network_page(self):
        frame = self.network_page

        # ------------------------
        # IP / PORT SECTION
        # ------------------------
        ttk.Label(frame, text="IP Address").pack(anchor="w", padx=10)

        self.ip_entry = ttk.Entry(frame)
        self.ip_entry.pack(fill="x", padx=10)

        ttk.Label(frame, text="Port").pack(anchor="w", padx=10, pady=(10, 0))

        self.port_entry = ttk.Entry(frame)
        self.port_entry.pack(fill="x", padx=10)

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=15)

        ttk.Button(
            btn_frame,
            text="Connect",
            command=self.connect_network
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame,
            text="Reconnect",
            command=self.reconnect
        ).pack(side="left", padx=5)


        # KEY MANAGEMENT
        ttk.Label(frame, text="Public Key").pack(anchor="w", padx=10)

        self.public_key_box = scrolledtext.ScrolledText(frame, height=6)
        self.public_key_box.pack(fill="x", padx=10)

        ttk.Label(frame, text="Private Key").pack(anchor="w", padx=10)

        self.private_key_box = scrolledtext.ScrolledText(frame, height=6)
        self.private_key_box.pack(fill="x", padx=10)

        ttk.Button(
            frame,
            text="Generate Keys",
            command=self.generate_keys,
        ).pack(pady=10)

        # Status log
        ttk.Label(frame, text="Network Logs").pack(anchor="w", padx=10)

        self.network_log = scrolledtext.ScrolledText(frame, height=8)
        self.network_log.pack(fill="both", expand=True, padx=10)

    def connect_network(self):
        ip = self.ip_entry.get()
        port = self.port_entry.get()

        self.network_log.insert(
            tk.END,
            f"Connecting to {ip}:{port}\n"
        )

        # ---------------------------
        # PLUG NETWORK CONNECT HERE
        # Example:
        # connect(ip, int(port))
        # ---------------------------

    def reconnect(self):
        self.network_log.insert(tk.END, "Reconnecting...\n")

        # Plug reconnect function here

    def generate_keys(self):
        self.network_log.insert(tk.END, "Generating RSA Keys...\n")

        # ---------------------------
        # PLUG KEY GENERATION HERE
        pub, priv = generate_rsa_keys()
        # Example:
        # pub, priv = generate_rsa_keys()
        # ---------------------------
        with open("private.pem", "r") as priv_file:
            private_pem = priv_file.read()
        with open("public.pem", "r") as pub_file:
            public_pem = pub_file.read()
        


        self.public_key_box.delete("1.0", tk.END)
        self.private_key_box.delete("1.0", tk.END)

        self.public_key_box.insert(tk.END,public_pem)
        self.private_key_box.insert(tk.END, private_pem)


# ==================================================
# RUN APP
# ==================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = HybridGUI(root)

    root.mainloop()