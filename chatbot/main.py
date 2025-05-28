import tkinter as tk
from Chatbot import Chatbot

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Eliza Chatbot")
        self.root.geometry("600x500")
        self.root.configure(bg="white")

        self.chatbot = Chatbot("c:/Users/FOTEINI TZOUMANI/Desktop/git/SafeScan/chatbot/intents.json")

        # Περιοχή συνομιλίας (μη επεξεργάσιμη)
        self.chat_display = tk.Text(root, bg="white", fg="black", font=("Arial", 12), wrap="word", state=tk.DISABLED)
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Περιοχή εισαγωγής
        self.user_input = tk.Entry(root, font=("Arial", 12))
        self.user_input.pack(side=tk.LEFT, padx=(10, 0), pady=10, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", lambda event: self.send_message())

        # Κουμπί αποστολής
        send_button = tk.Button(root, text="Στείλε", font=("Arial", 12), command=self.send_message, bg="#4CAF50", fg="white")
        send_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Μήνυμα έναρξης
        self.insert_message("Eliza", "Γεια σου! Πώς μπορώ να σε βοηθήσω;")

    def insert_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def send_message(self):
        user_text = self.user_input.get().strip()
        if user_text:
            self.insert_message("Εσύ", user_text)
            response = self.chatbot.get_response(user_text)
            self.insert_message("Eliza", response)
            self.user_input.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatbotGUI(root)
    root.mainloop()
