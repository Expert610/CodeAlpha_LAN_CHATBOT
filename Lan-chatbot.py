import threading
from tkinter import *
from tkinter import scrolledtext
import socket
from server import start_server  
import ttkbootstrap as ttk

threading.Thread(target=start_server, daemon=True).start()


chatbot_window = ttk.Window(themename="flatly")
chatbot_window.title("ChatBot")
chatbot_window.geometry("750x750")


client = socket.create_connection(("127.0.0.1", 12345))

def send_message():
    message = input_field.get().strip()
    if message:
        input_field.delete(0, END)
        display_message(f"User : {message}")
        client.send(message.encode())
        if message.lower() == "exit":
            client.close()
            chatbot_window.destroy()

def receive_messages():
    while True:
        try:
            response = client.recv(1024).decode()
            if response:
                display_message(f"Server : {response}")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def display_message(message):
    chat_area.config(state="normal")
    if message.startswith("Server :"):
        chat_area.insert(END, message + "\n", "right")
    elif message.startswith("User :"):
        chat_area.insert(END, message + "\n", "left")
    chat_area.config(state="disabled")
    chat_area.yview(END)


def clear_chat():
    chat_area.config(state="normal")
    chat_area.delete(1.0, END)
    chat_area.config(state="disabled")


chatbot_window.protocol("WM_DELETE_WINDOW", lambda: (client.close(), chatbot_window.destroy()))


ttk.Label(chatbot_window, text="Chat with ChatBot", font=("Arial", 20, "bold")).pack(pady=15)


chat_area = scrolledtext.ScrolledText(chatbot_window, 
                                      wrap=WORD, 
                                      state="disabled", 
                                      font=("Arial", 14),
                                      height=16)  
chat_area.pack(pady=10, padx=10)


chat_area.tag_configure("left", justify="left", foreground="green", lmargin1=10, lmargin2=10)
chat_area.tag_configure("right", justify="right", foreground="blue", rmargin=10)


input_frame = ttk.Frame(chatbot_window)
input_frame.pack(pady=10, padx=20, fill="x")


input_field = ttk.Entry(input_frame, font=("Arial", 16), width=50)
input_field.pack(padx=20,pady=10 ,ipadx=10, ipady=8)


send_button = ttk.Button(input_frame, text="Send" , command=send_message)
send_button.pack( padx=10)
clear_button = ttk.Button(chatbot_window, text="Clear Chat", command=clear_chat)
clear_button.pack(pady=5)

ttk.Label(text="Developed by Muhammad Yasir With 💖").pack(side=BOTTOM,padx=10,pady=20)



threading.Thread(target=receive_messages, daemon=True).start()


chatbot_window.mainloop()
