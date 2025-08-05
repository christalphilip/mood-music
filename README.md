# Mood Music Generator 🎵
Generate custom music based on your mood using Meta's MusicGen and natural language prompts!

## Overview
Mood Music Generator is a two‑part project:
1. **Python CLI + FastAPI Backend** — Fully functional, generates music clips from mood prompts using NLP and MusicGen.
2. **Android App** — An in‑progress mobile extension that integrates with the backend to provide an on‑the‑go music generation experience.

This project demonstrates skills in **natural language processing, transformer-based generative AI, Android development, and API integration**.

## Features

### Fully Functional (Python CLI + FastAPI Backend)
- Detects the mood you type (e.g., "joyful", "melancholy")
- Finds the closest match using WordNet synonyms
- Generates a custom music clip using Meta’s MusicGen transformer model
- Saves generated audio as `.wav` files for local playback
- REST API endpoints for generating and downloading audio

### In Progress (Android App)
- Mood selection UI **fully working** with backend API integration
- Basic audio playback of generated music
- Connects to local or ngrok‑exposed backend
- **Experimental:** Initial work on real‑time audio streaming (partial implementation)
- Planned: optimize generation speed, improve playback reliability, enhance error handling

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/christalphilip/mood-music.git
cd mood-music
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
import nltk 
nltk.download('wordnet')
```

### 3. CLI Usage
```bash
python mood-music.py
```
You will be prompted to enter your mood. The generated audio will be saved as a .wav file in the generated/ folder.

### 4. FastAPI Server Usage
```bash
uvicorn app:app --reload
```
Test endpoints in your browser: http://127.0.0.1:8000/docs

(Optional) Expose your local backend using ngrok
```bash
    ngrok http 8000
```
### 5. Android App (Frontend)
- Located in: android_app/
- Built with Kotlin + Android Studio
- Sends mood to FastAPI backend and plays generated audio

Make sure backend is running locally or deployed

Setup 
1. Open android_app/ in Android Studio
2. Update the API URL in MainActivity.kt to your backend IP
3. Build and run on emulator or physical device


## Project Structure
mood-music/
├── android_app/                 
│   └── MainActivity.kt          
├── app.py                      
├── mood_music.py                
├── generated/                  
├── README.md
├── LICENSE
└── .gitignore

## Project Status
- Python CLI + FastAPI backend: Fully functional and stable
- Android app: In‑progress extension with working UI, API calls, and basic playback
- Experimental: Partial implementation of real‑time audio streaming
- Next steps: Optimize CPU generation time, implement full streaming, improve playback handling, add robust error feedback

## License

This project is licensed under the [MIT License](LICENSE).
