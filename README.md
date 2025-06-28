# Lica - The WhatsApp AI Chatbot

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-maintenance--required-yellow.svg)

Lica is a Python-based chatbot designed to automatically reply to your WhatsApp messages. It uses **Selenium** for web automation to interact with WhatsApp Web and **ChatterBot** to generate human-like conversational responses.

The bot is designed to be smart: it only replies to **new messages in unmuted chats**, ignoring conversations you've silenced and preventing spammy behavior.

<br>

> 🚨 **VERY IMPORTANT DISCLAIMER: RISK OF BAN** 🚨
>
> Automating personal WhatsApp accounts is a violation of the **WhatsApp Terms of Service**. Using this bot, or any form of automation on your personal account, can result in a **permanent ban of your phone number**.
>
> **Use this project at your own risk.** It is highly recommended to use a test phone number that you do not mind losing. The author and contributors of this project are not responsible for any account bans or other consequences.

<br>

## Features

-   **Automatic Replies**: Automatically detects and replies to new, unread messages.
-   **Smart Detection**: Intelligently ignores chats that are muted, so it only interacts with conversations you deem important.
-   **Conversational AI**: Powered by `ChatterBot`, it learns from conversation corpora to provide relevant responses.
-   **Avoids Spam**: Keeps track of the last message processed to avoid sending duplicate replies to the same message.
-   **Configurable**: Easily trainable with different ChatterBot corpora to change its personality or language.

## Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

-   [Python 3.9](https://www.python.org/downloads/) or newer.
-   [Google Chrome](https://www.google.com/chrome/) browser.
-   A WhatsApp account (preferably a test account).

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/YOUR_USERNAME/LICA_REPOSITORY.git](https://github.com/YOUR_USERNAME/LICA_REPOSITORY.git)
    cd LICA_REPOSITORY
    ```

2.  **Create a virtual environment (recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required packages:**
    Create a file named `requirements.txt` and paste the following content into it:
    ```txt
    selenium
    webdriver-manager
    chatterbot==1.0.4
    spacy
    ```
    Now, run the installation command:
    ```sh
    pip install -r requirements.txt
    ```

4.  **Download the language model for SpaCy:**
    The ChatterBot library requires a language model for processing text. Run the following command to download the Portuguese model:
    ```sh
    python -m spacy download pt_core_news_sm
    ```

## Usage

1.  **First-Time Training (IMPORTANT):**
    The first time you run the bot, you need to train it. This creates a `db.sqlite3` database file with the conversation data.
    -   Open the Python script (`meu_bot_whatsapp.py`).
    -   Find the `__init__` method inside the `WhatsAppBot` class.
    -   **Uncomment** the lines related to training the bot:

        ```python
        # In __init__(self):
        if not os.path.exists('db.sqlite3'):
            print("INFO: Treinando o bot pela primeira vez. Isso pode levar alguns minutos...")
            trainer = ChatterBotCorpusTrainer(self.chatbot)
            trainer.train('chatterbot.corpus.portuguese')
            print("INFO: Treinamento concluído.")
        else:
            print("INFO: Banco de dados de treinamento já existe. Pulando treinamento.")
        ```
    -   Save the file.

2.  **Run the Bot:**
    Execute the script from your terminal:
    ```sh
    python meu_bot_whatsapp.py
    ```

3.  **Scan the QR Code:**
    -   A new Chrome browser window will open, displaying the WhatsApp Web QR code.
    -   On your phone, open WhatsApp and navigate to `Settings > Linked Devices > Link a Device`.
    -   Scan the QR code shown in the browser.

4.  **Let it Run:**
    Once you've logged in, the bot will start its main loop, checking for new messages every 10 seconds. Keep the terminal and the Chrome window open.

5.  **Subsequent Runs:**
    After the first run, you can **comment out the training lines again** to make the bot start up much faster, as it will use the existing `db.sqlite3` database.

## A Note on Selectors (Maintenance)

WhatsApp Web's front-end code changes frequently. This means the **CSS selectors** used in the script to find elements (like the "new message" dot or the message box) will eventually break.

If the bot stops working, you will likely need to update these selectors.

**How to find new selectors:**
1.  Open WhatsApp Web in your regular Chrome browser.
2.  Right-click on the element you want to find (e.g., the green dot for an unread chat) and click **"Inspect"**.
3.  The browser's Developer Tools will open, highlighting the element's HTML code.
4.  Look for stable attributes like `data-testid`, `id`, or a unique `class`. `data-testid` is usually the most reliable.
5.  Update the `By.CSS_SELECTOR` values in the Python script with the new selectors you've found. For example, if a message box selector changes, you would update this line:
    ```python
    # From:
    caixa_de_texto = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="old-selector"]')))
    # To:
    caixa_de_texto = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="new-selector-you-found"]')))
    ```

## Acknowledgments

-   Original concept and code by **Lucas sacb** (`@lucas_sacb`).
