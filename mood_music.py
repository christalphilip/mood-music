import os
import sys
import torch
import soundfile as sf
from transformers import AutoProcessor, MusicgenForConditionalGeneration
from nltk.corpus import wordnet as wn

# Device setup
device = "cuda" if torch.cuda.is_available() else "cpu"

# Predefined moods and music prompts
mood_to_prompt = {
    "happy": "upbeat pop music with bright piano, cheerful guitar, and energetic drums",
    "sad": "slow melancholic piano music with soft strings and gentle vocals",
    "angry": "intense rock music with heavy drums, distorted electric guitars, and aggressive vocals",
    "relaxed": "smooth jazz with saxophone, gentle bass, and soft drums",
    "anxious": "ambient electronic music with subtle synths, soft beats, and atmospheric sounds",
    "excited": "energetic dance music with strong bass, synth leads, and driving rhythm",
    "romantic": "soft acoustic ballad with warm guitar and tender vocals",
    "nostalgic": "retro synthwave with nostalgic synths and steady beats",
    "peaceful": "calm instrumental music with soft piano and soothing strings",
    "melancholy": "emotional piano and cello duet with slow tempo",
    "energetic": "fast-paced electronic music with powerful beats and bass",
    "hopeful": "uplifting orchestral music with bright brass and strings",
    "joyful": "cheerful acoustic guitar with lively percussion and happy vocals",
    "lonely": "soft ambient pads with sparse piano and echoing effects",
    "tired": "slow chillout lounge music with gentle synths and laid-back rhythm",
    "confident": "bold hip-hop beats with strong bass and catchy hooks",
    "thoughtful": "minimalist piano and strings with reflective mood",
    "playful": "bouncy ukulele and light percussion with a fun vibe",
    "determined": "driving rock music with powerful guitar riffs and steady drums",
}

def get_synonyms(word):
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower())
    return synonyms

def find_closest_mood(input_mood, known_moods):
    input_mood = input_mood.lower()
    if input_mood in known_moods:
        return input_mood
    for mood in known_moods:
        if input_mood in get_synonyms(mood):
            return mood
    return None

def main():
    # CLI argument or fallback to input
    if len(sys.argv) > 1:
        user_mood = sys.argv[1]
    else:
        user_mood = input("How is your mood today? ")

    closest_mood = find_closest_mood(user_mood, mood_to_prompt.keys())

    if closest_mood:
        music_prompt = mood_to_prompt[closest_mood]
    else:
        print("⚠️ Mood not recognized, generating default calm music.")
        closest_mood = "default"
        music_prompt = "calm instrumental music with soft piano and gentle strings"

    print("🎵 Music prompt:", music_prompt)

    # Load MusicGen model and processor
    musicgen_model = "facebook/musicgen-small"
    processor = AutoProcessor.from_pretrained(musicgen_model)
    model = MusicgenForConditionalGeneration.from_pretrained(musicgen_model).to(device)

    # Tokenize and generate audio
    inputs = processor(text=music_prompt, return_tensors="pt").to(device)
    audio_values = model.generate(**inputs, max_new_tokens=256)

    # Save output
    os.makedirs("generated", exist_ok=True)
    output_file = f"{closest_mood}.wav"
    output_path = os.path.join("generated", output_file)
    audio_array = audio_values[0].cpu().numpy()
    sf.write(output_path, audio_array.T, samplerate=32000)

    print("Generated file:", output_file)

if __name__ == "__main__":
    main()
