# 👷 Labor News Weekly Summarizer

Welcome! This app helps you quickly find and summarize the most important labor and economic news from the past week. It's designed to be easy to use, even if you've never written a line of code.

## 🌟 What this app does
- **Searches the web** for the latest labor news from trusted sources like CNBC, NBC, and the Bureau of Labor Statistics.
- **Uses AI (OpenAI)** to read through those news articles and write a professional summary for you.
- **Shows you the sources** in an easy-to-read table so you can verify the information.

---

## 🛠️ Getting Started (Setup)

Follow these simple steps to get the app running on your computer:

### 1. Open your Terminal
- **On Mac**: Press `Command + Space`, type "Terminal", and hit Enter.
- **On Windows**: Search for "PowerShell" or "Command Prompt" in your Start menu.

### 2. Go to the project folder
In your terminal, you need to "navigate" to where this project is saved. Type this command and hit Enter:
```bash
cd path/to/your/project-folder
```

### 3. Install the "helpers"
Your computer needs a few extra tools (libraries) to run the app. Type this command and hit Enter:
```bash
pip install -r requirements.txt
```
*Note: This might take a minute or two!*

---

## 🚀 How to Run the App

Once you've finished the setup above, you can start the app whenever you want:

1. In your terminal, type this command and hit Enter:
   ```bash
   streamlit run app.py
   ```
2. A new tab should automatically open in your web browser (like Chrome or Safari). If it doesn't, look at the terminal and click the link that looks like `http://localhost:8501`.

---

## 📖 How to Use the App

1. **Enter your API Key**: In the sidebar on the left, you'll see a box for an "OpenAI API Key". You'll need your own key from [OpenAI's website](https://platform.openai.com/api-keys). Paste it there.
2. **Fetch News**: Click the big **"🚀 Fetch & Summarize"** button in the middle of the screen.
3. **Read & Relax**: The app will search for news and generate a summary for you in seconds!

---

## ❓ Troubleshooting
- **"Command not found"**: Make sure you have Python installed.
- **"Invalid API Key"**: Double-check that you copied your OpenAI key correctly.
- **App won't load**: Ensure you ran the `pip install` command in Step 3 of the setup.

Enjoy staying up to date with labor news!
