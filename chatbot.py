import tkinter as tk
from tkinter import scrolledtext
import requests
from datetime import datetime

API_URL = "https://en.wikipedia.org/w/api.php"

HEADERS = {
    "User-Agent": "AnjaliSmartChatbot/1.0 (Python educational project)"
}


def get_greeting(question):
    message = question.lower().strip().rstrip("?!., ")

    greetings = {
        "hi": "Hello! How can I help you?",
        "hello": "Hey! Nice to meet you.",
        "hey": "Hey there! What would you like to know?",
        "good morning": "Good morning! Have a great day.",
        "good afternoon": "Good afternoon! How can I help you?",
        "good evening": "Good evening! What can I do for you?",
        "how are you": "I'm doing great! Thanks for asking.",
        "thank you": "You're welcome! Happy to help.",
        "thanks": "You're welcome!",
        "who are you": "I'm your Smart AI Chatbot.",
        "what can you do": "I can answer questions, respond to greetings, and save our chat history."
    }

    return greetings.get(message)


def get_answer(question):
    try:
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": question,
            "format": "json"
        }

        response = requests.get(
            API_URL,
            params=search_params,
            headers=HEADERS,
            timeout=15
        )
        response.raise_for_status()

        results = response.json().get("query", {}).get("search", [])

        if not results:
            return "Sorry, I couldn't find an answer."

        page_title = results[0]["title"]

        extract_params = {
            "action": "query",
            "prop": "extracts",
            "explaintext": 1,
            "exintro": 1,
            "titles": page_title,
            "format": "json"
        }

        response = requests.get(
            API_URL,
            params=extract_params,
            headers=HEADERS,
            timeout=15
        )
        response.raise_for_status()

        pages = response.json().get("query", {}).get("pages", {})

        for page in pages.values():
            answer = page.get("extract", "")
            if answer:
                return answer[:1500]

        return "I found a page, but no summary is available."

    except requests.exceptions.Timeout:
        return "Search timed out. Please try again."

    except requests.exceptions.ConnectionError:
        return "Internet connection problem. Check your network."

    except requests.exceptions.RequestException:
        return "Unable to connect to Wikipedia right now."

    except Exception as error:
        return f"Unexpected error: {error}"


def save_chat(question, answer):
    with open("chat_history.txt", "a", encoding="utf-8") as file:
        file.write(f"\nDate: {datetime.now()}\n")
        file.write(f"You: {question}\n")
        file.write(f"Bot: {answer}\n")
        file.write("-" * 50 + "\n")


def display_message(sender, message):
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"{sender}: {message}\n\n")
    chat_area.config(state=tk.DISABLED)
    chat_area.see(tk.END)


def send_message():
    question = message_entry.get().strip()

    if not question:
        return

    message_entry.delete(0, tk.END)
    display_message("You", question)

    if question.lower() in ["exit", "quit", "bye"]:
        display_message("Bot", "Thank you for chatting. Goodbye!")
        save_chat(question, "Thank you for chatting. Goodbye!")
        root.after(1500, root.destroy)
        return

    if question.lower() == "history":
        try:
            with open("chat_history.txt", "r", encoding="utf-8") as file:
                history = file.read()

            display_message(
                "Bot",
                history if history.strip() else "No chat history available."
            )
        except FileNotFoundError:
            display_message("Bot", "No previous chat history found.")
        return

    answer = get_greeting(question)

    if answer is None:
        display_message("Bot", "Searching...")
        root.update_idletasks()
        answer = get_answer(question)

        # Remove the temporary Searching message
        chat_area.config(state=tk.NORMAL)
        content = chat_area.get("1.0", tk.END)
        chat_area.delete("1.0", tk.END)
        chat_area.insert(tk.END, content.replace("Bot: Searching...\n\n", "", 1))
        chat_area.config(state=tk.DISABLED)

    display_message("Bot", answer)
    save_chat(question, answer)


# Main GUI window
root = tk.Tk()
root.title("Smart AI Chatbot")
root.geometry("750x600")
root.minsize(500, 400)
root.configure(bg="#202A44")

# Heading
heading = tk.Label(
    root,
    text="SMART AI CHATBOT",
    font=("Arial", 22, "bold"),
    bg="#202A44",
    fg="white"
)
heading.pack(pady=15)

# Chat display area
chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Arial", 11),
    bg="#F4F6FA",
    fg="#202A44",
    padx=12,
    pady=12,
    state=tk.DISABLED
)
chat_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

display_message("Bot", "Welcome! Ask me anything.")
display_message("Bot", "Type 'history' to view previous conversations.")
display_message("Bot", "Type 'exit' to close the chatbot.")

# Input frame
input_frame = tk.Frame(root, bg="#202A44")
input_frame.pack(fill=tk.X, padx=20, pady=15)

message_entry = tk.Entry(
    input_frame,
    font=("Arial", 12),
    relief=tk.FLAT
)
message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10)
message_entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(
    input_frame,
    text="Send",
    font=("Arial", 11, "bold"),
    bg="#2878D0",
    fg="white",
    relief=tk.FLAT,
    padx=20,
    command=send_message
)
send_button.pack(side=tk.LEFT, padx=8)

exit_button = tk.Button(
    root,
    text="Exit",
    font=("Arial", 10, "bold"),
    bg="#D9534F",
    fg="white",
    relief=tk.FLAT,
    padx=25,
    command=root.destroy
)
exit_button.pack(pady=(0, 15))

message_entry.focus()
root.mainloop()