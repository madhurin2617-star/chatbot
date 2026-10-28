
import tkinter as tk
from tkinter import scrolledtext
import requests

API = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "MadhuriSmartChatbot/1.0"}
HISTORY = "chat_history.txt"


def reply(message):
    text = message.lower().strip().rstrip("?!., ")

    greetings = {
        "hi": "Hello! How can I help you?",
        "hello": "Hey! Nice to meet you.",
        "hey": "Hi there!",
        "how are you": "I'm fine, thanks for asking!",
        "thank you": "You're welcome!",
        "thanks": "Happy to help!",
        "who are you": "I'm your Smart Chatbot.",
        "what can you do": "I can chat and search Wikipedia."
    }
    if text in greetings:
        return greetings[text]

    # Clean common question phrases
    query = text
    for prefix in ("what is ", "who is ", "tell me about ", "define "):
        if query.startswith(prefix):
            query = query[len(prefix):]
            break
    query = query.rstrip("?., ").strip()

    try:
        r = requests.get(API, params={
            "action": "query", "list": "search",
            "srsearch": query, "srlimit": 5, "format": "json"
        }, headers=HEADERS, timeout=10)
        r.raise_for_status()
        results = r.json().get("query", {}).get("search", [])

        if not results:
            return "Sorry, no information found. Try another question."

        title = results[0]["title"]
        # Prefer an exact page title match
        for item in results:
            if item["title"].casefold() == query.casefold():
                title = item["title"]
                break

        r = requests.get(API, params={
            "action": "query", "prop": "extracts",
            "explaintext": 1, "exintro": 1,
            "titles": title, "format": "json"
        }, headers=HEADERS, timeout=10)
        r.raise_for_status()

        for page in r.json().get("query", {}).get("pages", {}).values():
            answer = page.get("extract", "").strip()
            if answer:
                return f"Topic: {title}\n{answer[:1000]}"

        return f"No summary available for {title}."

    except requests.exceptions.RequestException:
        return "Internet connection problem. Please try again."


def show(sender, message):
    chat.config(state=tk.NORMAL)
    chat.insert(tk.END, f"{sender}: {message}\n")
    chat.config(state=tk.DISABLED)
    chat.see(tk.END)


def save_history(question, answer):
    try:
        with open(HISTORY, "a", encoding="utf-8") as f:
            f.write(f"You: {question}\nBot: {answer}\n\n")
    except OSError:
        pass


def send(event=None):
    question = entry.get().strip()
    if not question:
        return

    entry.delete(0, tk.END)
    show("You", question)

    if question.lower() in ("bye", "exit", "quit"):
        show("Bot", "Thank you for chatting. Goodbye!")
        save_history(question, "Goodbye!")
        root.after(1000, root.destroy)
        return

    if question.lower() == "history":
        try:
            with open(HISTORY, encoding="utf-8") as f:
                old = f.read().strip()
            show("Bot", old or "No chat history yet.")
        except FileNotFoundError:
            show("Bot", "No chat history yet.")
        return

    answer = reply(question)
    show("Bot", answer)
    save_history(question, answer)


def clear_chat():
    chat.config(state=tk.NORMAL)
    chat.delete("1.0", tk.END)
    chat.config(state=tk.DISABLED)
    show("Bot", "Chat cleared. Ask me anything!")


root = tk.Tk()
root.title("Smart AI Chatbot")
root.geometry("750x600")
root.minsize(500, 400)
root.configure(bg="#202A44")

tk.Label(root, text="SMART AI CHATBOT",
         font=("Arial", 22, "bold"),
         bg="#202A44", fg="white").pack(pady=12)

chat = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, font=("Arial", 11),
    bg="#F4F6FA", fg="#202A44",
    padx=12, pady=12, state=tk.DISABLED
)
chat.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

show("Bot", "Welcome! Ask me anything.")
show("Bot", "Type 'history' to view chats or 'bye' to exit.")

frame = tk.Frame(root, bg="#202A44")
frame.pack(fill=tk.X, padx=20, pady=10)

entry = tk.Entry(frame, font=("Arial", 12))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=9)
entry.bind("<Return>", send)

tk.Button(frame, text="Send", command=send,
          bg="#2878D0", fg="white", padx=18).pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Clear Chat", command=clear_chat,
          bg="#E0A52B", fg="black").pack(side=tk.LEFT)

tk.Button(root, text="Exit", command=root.destroy,
          bg="#D9534F", fg="white", padx=25).pack(pady=(0, 12))

entry.focus()
root.mainloop()
