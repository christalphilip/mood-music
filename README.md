# Mood Music Generator 

Generate music based on your mood using Meta's MusicGen and natural language prompts!

## Features
- Detects the mood you type (e.g., "joyful", "melancholy", etc.)
- Finds the closest match using WordNet synonyms
- Generates a custom music clip using a transformer model
- Android app frontend to input mood and stream/download audio
- FastAPI backend to serve or generate audio


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
Open in browser: http://127.0.0.1:8000/docs to test the /generate_music/ and /download/{filename} endpoints.

### 5. Android App (Frontend)
- Located in: android_app/
- Built with Kotlin + Android Studio
- Sends mood to FastAPI backend and streams/generated music

Make sure backend is running locally or deployed

Setup 
1. Open android_app/ in Android Studio
2. Update the API URL in MainActivity.kt to your backend IP
3. Build and run on emulator or physical device


### Project Structure
mood-music/
├── android_app/                 # Android frontend app
│   └── MainActivity.kt          # Main app logic
├── app.py                       # FastAPI backend
├── mood_music.py                # CLI tool
├── generated/                   # Output .wav files
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
            

## License

This project is licensed under the [MIT License](LICENSE).
