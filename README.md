# Mood Music Generator 

Generate music based on your mood using Meta's MusicGen and natural language prompts!

## Features
- Detects the mood you type (e.g., "joyful", "melancholy", etc.)
- Finds the closest match using WordNet synonyms
- Generates a custom music clip using a transformer model


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

### Usage
```bash
python mood-music.py
```
You will be prompted to enter your mood. The generated audio will be saved as a .wav file.

### Example Outputs

Two example outputs are included in the example_outputs/ folder.


### Project Structure
mood-music/
├── mood_music.py               
├── requirements.txt            
├── README.md                   
├── LICENSE                    
├── .gitignore                 
└── example_outputs/
    └── happy.wav 
    └-- melancholy.wav             


## License

This project is licensed under the [MIT License](LICENSE).
