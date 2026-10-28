# Smart AI Chatbot 🤖

## About the Project

Smart AI Chatbot is a Python-based desktop application that allows users to interact with a chatbot through a simple graphical user interface (GUI). It responds to greetings and retrieves information from Wikipedia based on user questions.

## Features

- User-friendly graphical interface using Tkinter
- Responds to greetings and common messages
- Searches Wikipedia for information
- Displays chatbot responses in a scrollable chat window
- Saves conversation history in a text file
- Allows users to view previous chat history
- Includes Send and Exit buttons
- Handles internet connection and request timeout errors

## Technologies Used

- Python
- Tkinter
- Requests
- Wikipedia API

## Requirements

- Python 3 installed
- Internet connection for Wikipedia searches
- `requests` Python package

## Installation and Execution

1. Install Python 3.

2. Install the required package:

   ```bash
   python -m pip install requests
   ```

3. Download or clone this repository.

4. Open Command Prompt in the project folder.

5. Run the application:

   ```bash
   python chatbot.py
   ```

## How to Use

1. Launch the application.
2. Type a greeting or question in the message box.
3. Click **Send** or press Enter.
4. Type `history` to view saved conversations.
5. Type `bye`, `exit`, or `quit` to close the chatbot.

## Project Structure

```text
Chatbot/
├── chatbot.py
├── README.md
└── chat_history.txt
```

*Note: `chat_history.txt` is generated when conversations are saved. It may not exist until the chatbot is used.*

## How It Works

The chatbot first checks whether the user's message matches a predefined greeting. If no greeting matches, it searches Wikipedia through the MediaWiki API and retrieves a page summary. Conversations are saved locally in a text file.

## Limitations

- Answers depend on information available through Wikipedia.
- An internet connection is required for information searches.
- This is a rule-based chatbot with Wikipedia integration, not a generative AI model.

## Author

GitHub:https://github.com/madhurin2617-star

## License

This project is intended for educational purposes.
