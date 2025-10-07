# YouTube Audio Transcriber, Summarizer & Translator

## 📘 Project Description
This project is a **Streamlit-based web application** that allows users to:  
1. Download audio from YouTube videos.  
2. Convert the audio to text using **speech recognition**.  
3. Summarize the transcript using **BART transformer-based NLP models**.  
4. Translate the summary into multiple languages using **Google Translate API**.

It’s designed for **efficient content consumption** and **multi-language accessibility**, making it ideal for students, researchers, and content creators.

---

## ⚙️ Tech Stack
- **Python** – Programming language  
- **Streamlit** – Web application framework  
- **yt-dlp** – YouTube video/audio downloader  
- **pydub** – Audio processing  
- **SpeechRecognition** – Speech-to-text conversion  
- **Transformers (HuggingFace)** – Text summarization (BART model)  
- **Googletrans** – Translation API  
- **Regex** – Text cleaning  

---

## 🧠 Features
- Download audio from any public YouTube video  
- Automatic audio-to-text transcription in chunks  
- Summarization of long transcripts  
- Translation of summaries into multiple languages (Spanish, French, German, Chinese, Hindi)  
- Clean UI via Streamlit for easy user interaction  

---

## 🚀 Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/Vashishtha-11/T.Y_Project.git
cd T.Y_Project

Create a virtual environment

python -m venv .venv


Activate the virtual environment

Windows (PowerShell):

.venv\Scripts\Activate.ps1


Windows (CMD):

.venv\Scripts\activate.bat


macOS/Linux:

source .venv/bin/activate


Install dependencies

pip install -r requirements.txt


Run the Streamlit app

streamlit run app.py

🧾 Usage

Enter the YouTube video URL in the app.

Wait for the audio to be downloaded and processed.

View the full transcript.

View the summarized transcript.

Select a language and click Translate Summary to get the translated version.

⚡ Notes

Ensure you have internet access for YouTube downloading and Google Translate.

The .venv folder and downloads/ folder are ignored in Git.

For best results, use videos with clear audio.

📁 Folder Structure
T.Y_Project/
│
├─ app.py                  # Main Streamlit application
├─ requirements.txt        # Python dependencies
├─ README.md               # Project documentation
├─ .gitignore              # Ignored files and folders
├─ downloads/              # Folder for downloaded audio (ignored in Git)
└─ .venv/                  # Python virtual environment (ignored in Git)

🌐 Author

Vashishtha Sagvekar – B.Tech AI & ML student
GitHub

