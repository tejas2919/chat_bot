# 🤖 Claude Chat Application

A ChatGPT-like interface with voice support, built using Streamlit and the Anthropic Claude API.

#MENTOR 
-MS.ANKITA MAM-Faculty Guide 
-DR.RAJESHUPADHYAY-Head of Departement (HOD)

#TEAM MEMBERS



## ✨ Features

- 💬 Text-based chat interface
- 🎤 Voice input support
- 📝 Chat history export
- 🎨 Clean, modern UI
- 🔒 Secure API key management
- 🚀 One-click deployment to Render

## 🛠 Tech Stack

- Backend: Python
- Frontend: Streamlit
- APIs: Anthropic Claude API, Google Speech Recognition
- Voice Input: speech_recognition + PyAudio
- Env Management: python-dotenv

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/claude-chat.git
cd claude-chat
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

5. Run the application:
```bash
streamlit run app.py
```

## 🎤 Voice Input Setup

- Windows:
```bash
pipwin install pyaudio
```

- Linux:
```bash
sudo apt-get install python3-pyaudio
```

- macOS:
```bash
brew install portaudio
pip install pyaudio
```

## 🚀 Deployment on Render

1. Fork this repository
2. Create a new Web Service on Render
3. Connect your repository
4. Set the environment variable `ANTHROPIC_API_KEY`
5. Deploy

## 📝 Usage

1. Type your message or use voice input
2. Click send or press Enter
3. View AI response in the chat
4. Export chat history if needed

## ⚠ Error Handling

The application handles various error cases:
- Invalid API key
- Network issues
- Microphone access problems
- Empty messages

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 
