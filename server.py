import socket
import random
from nltk.chat.util import Chat,reflections



pairs = [
    (r".*\b(hello|hi|hey|whats up|yo|greeting)\b.*", ["Hello! How can I help you?"]),
    (r".*\b(how are you|how|ok|where|where you from)\b.*", ["I'm good, thanks for asking!", " I'm doing fine!"]),
    (r".*\b(what is your name|what your name|your name|name|tell name)\b.*", ["I'm a LAN chatbot."]),
    (r".*\b(bye|good bye|thek)\b.*", ["Goodbye! Have a great day!","Have a nice day!"]),
    (r".*\b(who made you|who made|made by|who are you|developed by|develop by|who develop you)\b.*", ["Developed by Muhammad Yasir With 💖!"]),
]


custom_response = {
    "good": ["That's good to hear! How can I assist you?"],
    "good morning":["Good morning,Hope you have a great day"],
    "good evening":["Good evening ,You have a nice day"],
    "please help":["What i do for you"],
    "please":["ok i do"],
    "thanks you":["It's my pleasure"],
    "thank":["its my pleasure"],
    "job":["I am glad to hear that"],
    "bad": ["I'm sorry to hear that. Do you want to talk about it?"],
    "security": ["Yes, security is very important! Some key aspects include encryption, authentication, and strong passwords."],
    "hacking": ["Hacking can be ethical or unethical. Ethical hacking helps protect systems from threats."],
    "ai": ["AI is transforming the world! It powers chatbots like me, self-driving cars, and much more."],
    "programming": ["Programming is a great skill! Do you have a favorite language?"],
}


fallback_responses = [
    "That sounds interesting! Tell me more.",
    "I haven't heard about that before, can you explain?",
    "Oh, really? I'd like to learn more!",
    "Hmm, I'm not sure about that, but I'm listening!",
    "I only answer a Predefined Words or Sentences",
    "I have no Knowledge about that",
]

chatbot = Chat(pairs, reflections)


def generate_response(user_input):
    response = chatbot.respond(user_input)
    if response:
        return response 

    
    for keyword, replies in custom_response.items():
        if keyword in user_input.lower():
            return random.choice(replies)

    
    return random.choice(fallback_responses)


def start_server():
    
    server = socket.create_server(("127.0.0.1", 12345))
    print("Chatbot Server Running... (Press Ctrl+C to stop)")


    print("Waiting for connections...")
    def handle_client(client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    print(f"Received: {message}")
                    response = generate_response(message)
                    client_socket.send(response.encode())
            except:
                print("Client disconnected")
                client_socket.close()
                break

    
    client_socket, addr = server.accept()
    print(f"Connection established with {addr}")
    
    handle_client(client_socket)
 
