import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import soundfile as sf
from nltk.corpus import wordnet

# Force device to CPU
device = "cpu"
print(f"Device set to use {device}")

# Mood to music prompt dictionary
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

# Use WordNet to get synonyms in case exact word isn't found in dictionary
def get_synonyms(word):
    syns = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            syns.add(lemma.name().lower().replace("_", " "))
    return syns

# Match up closest mood from dictionary 
def find_closest_mood(user_mood, mood_keys):
    user_mood = user_mood.lower()
    user_words = user_mood.split()
    user_syns = set()
    # Splits input into words, finds synonyms for each word, then combines
    for w in user_words:
        user_syns.update(get_synonyms(w))
        user_syns.add(w)
    # Checks overlap between synonyms
    for mood in mood_keys:
        mood_syns = get_synonyms(mood)
        mood_syns.add(mood)

        if user_syns.intersection(mood_syns):
            return mood
    return None

# Generate music prompt 
def main():
    user_mood = input("How is your mood today? ")
    closest_mood = find_closest_mood(user_mood, mood_to_prompt.keys())
    # Set default if music isn't recognized
    if closest_mood:
        music_prompt = mood_to_prompt[closest_mood]
    else:
        print("⚠️ Mood not recognized, generating default calm music.")
        music_prompt = "calm instrumental music with soft piano and gentle strings"
    print("🎵 Music prompt for generation:", music_prompt)

    # Load MusicGen model and processor
    musicgen_model = "facebook/musicgen-small"
    processor = AutoProcessor.from_pretrained(musicgen_model)
    musicgen = MusicgenForConditionalGeneration.from_pretrained(musicgen_model).to(device)
    # Convert prompt into tensors 
    inputs = processor(text=music_prompt, return_tensors="pt").to(device)
    # Generates audio output using model
    audio_tensor = musicgen.generate(**inputs, max_new_tokens=256)
    
    # Saves output wav file
    output_file = f"{closest_mood if closest_mood else 'default'}.wav"
    audio_np = audio_tensor[0].cpu().numpy()    # Converts into NumPy array to save
    sf.write(output_file, audio_np.T, 32000)
    print("✅ Music generated and saved to:", output_file)
# Runs main
if __name__ == "__main__":
    main()
