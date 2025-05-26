import tkinter as tk
from Chatbot import Chatbot

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Eliza - Chatbot")
        self.root.geometry("500x600")
        
        self.chatbot = Chatbot("intents.json")

        self.chat_log = tk.Text(root, bd=1, bg="white", height=20, width=50, wrap="word")
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.pack(pady=10)

        self.entry_box = tk.Entry(root, bd=1, bg="lightgray", width=40)
        self.entry_box.pack(pady=10, padx=10, side=tk.LEFT, expand=True, fill=tk.X)

        self.send_button = tk.Button(root, text="Στείλε", command=self.send_message)
        self.send_button.pack(padx=10, pady=10, side=tk.RIGHT)

        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, "Eliza: Γεια σου! Πως μπορώ να σε βοηθήσω;\n")
        self.chat_log.config(state=tk.DISABLED)

    def send_message(self):
        user_input = self.entry_box.get()
        if user_input.strip():
            self.chat_log.config(state=tk.NORMAL)
            self.chat_log.insert(tk.END, f"Εσύ: {user_input}\n")
            response = self.chatbot.get_response(user_input)
            self.chat_log.insert(tk.END, f"Eliza: {response}\n\n")
            self.chat_log.config(state=tk.DISABLED)
            self.entry_box.delete(0, tk.END)
            self.chat_log.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatbotGUI(root)
    root.mainloop()
