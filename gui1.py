import customtkinter as ctk
from tkinter import filedialog, messagebox
from hybrid_chat import *
from hybrid_file import *


#     encrypt_file,
#     decrypt_file,
#     encrypt_message,
#     decrypt_message,
#     generate_rsa_keys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1000x700")
app.title("Hybrid Encryption System")


# CHAT HISTORY STORAGE

chat_history = []


# TAB SYSTEM

tabview = ctk.CTkTabview(app)
tabview.pack(fill="both", expand=True, padx=20, pady=20)

tabview.add("Secure Chat")
tabview.add("File Encryption")
tabview.add("Key Management")


chat_tab = tabview.tab("Secure Chat")

ctk.CTkLabel(chat_tab, text="Chat History").pack(pady=5)

chat_display = ctk.CTkTextbox(chat_tab, width=900, height=350)
chat_display.pack(pady=10)
chat_display.configure(state="disabled")

ctk.CTkLabel(chat_tab, text="Enter Message").pack()

message_box = ctk.CTkTextbox(chat_tab, width=900, height=100)
message_box.pack(pady=10)


# UPDATE CHAT DISPLAY

def refresh_chat():
    chat_display.configure(state="normal")
    chat_display.delete("1.0", "end")

    for msg in chat_history:
        chat_display.insert("end", msg + "\n\n")

    chat_display.configure(state="disabled")



# ENCRYPT MESSAGE

def gui_encrypt_message():
    message = message_box.get("1.0", "end").strip()

    if not message:
        messagebox.showerror("Error", "Enter a message")
        return

    encrypted, encrypted_key = hb_encrypt(message)

    chat_history.append(f"YOU: {message}")
    chat_history.append(f"ENCRYPTED: {encrypted}")

    refresh_chat()
    message_box.delete("1.0", "end")



# DECRYPT MESSAGE

def gui_decrypt_message():
    message = message_box.get("1.0", "end").strip()

    if not message:
        messagebox.showerror("Error", "Enter encrypted text")
        return

    # PLUG IN YOUR FUNCTION HERE
    decrypted = hb_decryption(message,encrypted_key)
   

    chat_history.append(f"DECRYPTED: {decrypted}")

    refresh_chat()
    message_box.delete("1.0", "end")


ctk.CTkButton(
    chat_tab,
    text="Encrypt Message",
    command=gui_encrypt_message
).pack(pady=5)

ctk.CTkButton(
    chat_tab,
    text="Decrypt Message",
    command=gui_decrypt_message
).pack(pady=5)

# FILE ENCRYPTION TAB

file_tab = tabview.tab("File Encryption")

selected_file = ctk.StringVar()

def choose_file():
    file = filedialog.askopenfilename()
    selected_file.set(file)

def gui_encrypt_file():
    file_path = selected_file.get()

    if not file_path:
        messagebox.showerror("Error", "Select a file first")
        return

    encrypt_file(file_path)
  

    messagebox.showinfo("Success", "File encrypted")


def gui_decrypt_file():
    file_path = selected_file.get()

    if not file_path:
        messagebox.showerror("Error", "Select a file first")
        return
#plug in fn
    decrypt_file(file_path)
    messagebox.showinfo("Success", "File decrypted")


ctk.CTkEntry(file_tab, textvariable=selected_file, width=700).pack(pady=10)

ctk.CTkButton(file_tab, text="Choose File", command=choose_file).pack(pady=5)
ctk.CTkButton(file_tab, text="Encrypt File", command=gui_encrypt_file).pack(pady=5)
ctk.CTkButton(file_tab, text="Decrypt File", command=gui_decrypt_file).pack(pady=5)


key_tab = tabview.tab("Key Management")

def gui_generate_keys():

    generate_rsa_keys()
   

    messagebox.showinfo("Success", "RSA Keys Generated")


ctk.CTkButton(
    key_tab,
    text="Generate RSA Keys",
    command=gui_generate_keys
).pack(pady=20)


app.mainloop()