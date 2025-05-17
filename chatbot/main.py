from Chatbot import Chatbot 
import hashlib


if __name__ == "__main__":
    chatbot = Chatbot("intents.json")

    print("Γεια σου! Πως μπορω να σε βοηθήσω; ")
    while True:
        user_input = input("Εσυ:")
        if user_input.lower() == "εξοδος":
            print("Chatbot:Τα λεμε!")
            break
        response = chatbot.get_response(user_input)
        print("Chatbot:",response)