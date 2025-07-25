from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
import subprocess
import os

app = FastAPI()

GENERATED_DIR = "generated"
os.makedirs(GENERATED_DIR, exist_ok=True)

def generate_music_for_mood(mood: str) -> str:
    filename = f"{mood}.wav"
    file_path = os.path.join(GENERATED_DIR, filename)

    # Step 1: Check if the file already exists
    if os.path.exists(file_path):
        print(f"✅ Found pre-generated file: {file_path}")
        return filename

    # Step 2: Run mood_music.py only if file doesn't exist
    print(f"⚙️ Generating new music for mood: {mood}")
    result = subprocess.run(["python3", "mood_music.py", mood],
                            capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ Error:", result.stderr)
        raise RuntimeError("Music generation failed")

    # Step 3: Extract the filename from script output
    for line in result.stdout.splitlines():
        if line.startswith("Generated file:"):
            generated_file = line.split("Generated file:")[-1].strip()
            print(f"✅ Returning generated file: {generated_file}")
            return generated_file

    raise RuntimeError("Filename not found in script output")


    # Extract the filename from the output
    for line in result.stdout.splitlines():
        if line.startswith("Generated file:"):
            filename = line.split("Generated file:")[-1].strip()
            print(f"Returning file: {filename}")
            return filename

    raise RuntimeError("Filename not found in script output")

@app.get("/generate_music/")
async def generate_music(mood: str = Query(...)):
    try:
        filename = generate_music_for_mood(mood)
        download_url = f"/download/{filename}"
        return {"status": "success", "download_url": download_url}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(GENERATED_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/wav", filename=filename)
    return JSONResponse(status_code=404, content={"detail": "File not ready"})
