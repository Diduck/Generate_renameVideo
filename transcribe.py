from faster_whisper import WhisperModel
import os, glob

VIDEOS_DIR = r"d:\10_RESSOURCE\PROJETS\Generate_renameVideo\Videos"
TRANSCRIPTS_DIR = r"d:\10_RESSOURCE\PROJETS\Generate_renameVideo\Transcripts"
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

model = WhisperModel("medium", device="cpu", compute_type="int8")

files = sorted(glob.glob(os.path.join(VIDEOS_DIR, "*.MOV")) + glob.glob(os.path.join(VIDEOS_DIR, "*.mov")))
print(f"Found {len(files)} video files to transcribe.\n")

for f in files:
    name = os.path.splitext(os.path.basename(f))[0]
    out_path = os.path.join(TRANSCRIPTS_DIR, name + ".txt")
    if os.path.exists(out_path):
        print(f"[SKIP] {name} (already transcribed)")
        continue
    print(f"[TRANSCRIBING] {name}...")
    try:
        segments, info = model.transcribe(f, language="fr", beam_size=5)
        text = "\n".join(seg.text.strip() for seg in segments)
        with open(out_path, "w", encoding="utf-8") as fout:
            fout.write(text)
        print(f"  -> Done ({info.duration:.0f}s audio)")
    except Exception as e:
        print(f"  -> ERROR: {e}")

print("\nAll done.")
