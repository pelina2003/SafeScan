import tkinter as tk
from tkinter import messagebox
from forum_controller import ForumController

class ForumView:
    def __init__(self, user):
        self.user = user
        self.controller = ForumController()

        self.root = tk.Tk()
        self.root.title("Φόρουμ Συζητήσεων")
        self.root.geometry("600x500")

        # Κουμπί εκκίνησης: εμφανίζει τη λίστα διαθέσιμων φόρουμ
        self.btn_open_forums = tk.Button(self.root, text="Φόρουμ Συζητήσεων", command=self.open_forum_list)
        self.btn_open_forums.pack(pady=10)

        # Λίστα με διαθέσιμα φόρουμ (εμφανίζεται μετά το πάτημα του κουμπιού)
        self.forum_listbox = tk.Listbox(self.root, width=80)
        self.forum_listbox.bind("<<ListboxSelect>>", self.on_forum_selected)

        # Περιοχή εμφάνισης μηνυμάτων
        self.messages_text = tk.Text(self.root, height=12, state="disabled")

        # Πεδίο και κουμπί αποστολής μηνύματος
        self.entry = tk.Entry(self.root, width=60)
        self.btn_send = tk.Button(self.root, text="Αποστολή Μηνύματος", command=self.send_message)

        self.current_forum_id = None
        self.forums = []

        self.root.mainloop()

    def open_forum_list(self):
        self.forums = self.controller.get_all_forums()
        if not self.forums:
            messagebox.showinfo("Πληροφορία", "Δεν υπάρχουν διαθέσιμα φόρουμ προς το παρόν.")
            return
        self.forum_listbox.delete(0, tk.END)
        for f in self.forums:
            self.forum_listbox.insert(tk.END, f"{f.topic} ({f.location})")

        self.forum_listbox.pack(pady=5)
        self.messages_text.pack(pady=5)

    def on_forum_selected(self, event):
        selection = self.forum_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        forum = self.forums[index]
        self.current_forum_id = forum.id
        self.display_messages(forum.id)

        # Ενεργοποίηση εισαγωγής και αποστολής
        self.entry.pack(pady=5)
        self.btn_send.pack()

    def display_messages(self, forum_id):
        self.messages_text.config(state="normal")
        self.messages_text.delete("1.0", tk.END)
        messages = self.controller.get_messages_for_forum(forum_id)
        for m in messages:
            self.messages_text.insert(tk.END, f"{m.author}: {m.content}\n")
        self.messages_text.config(state="disabled")

    def send_message(self):
        if not self.current_forum_id:
            messagebox.showerror("Σφάλμα", "Δεν έχει επιλεγεί φόρουμ.")
            return
        content = self.entry.get().strip()
        if not content:
            return
        success = self.controller.submit_message(self.current_forum_id, self.user, content)
        if not success:
            messagebox.showerror("Σφάλμα", "Το μήνυμα δεν αποθηκεύτηκε. Παρακαλώ προσπαθήστε ξανά.")
        else:
            self.entry.delete(0, tk.END)
            self.display_messages(self.current_forum_id)
