import os
import subprocess
from music21 import stream, note, tempo
from pydub import AudioSegment

# Install dependencies if missing
try:
    import music21
except ImportError:
    subprocess.check_call(["pip", "install", "music21", "pydub"])

# Step 1: Generate melody from BPM
def generate_melody(bpm, num_bars=4):
    """
    Generate a simple melody based on BPM.
    Returns path to generated MIDI file.
    """
    melody = stream.Stream()
    melody.append(tempo.MetronomeMark(number=bpm))

    scale_notes = ["C4", "E4", "G4", "A4", "F4", "D4", "B4", "C5"]
    for _ in range(num_bars * 4):  # 4 beats per bar
        melody.append(note.Note(scale_notes[_ % len(scale_notes)], quarterLength=1))

    midi_path = "generated_melody.mid"
    melody.write("midi", fp=midi_path)
    return midi_path

# Step 2: Generate singing from lyrics + melody using DiffSinger
def synthesize_singing(lyrics, bpm, beat_file=None, output_file="final_song.wav"):
    """
    Create AI singing from lyrics and BPM, optionally mixing with a beat track.
    """
    # Generate melody
    midi_path = generate_melody(bpm)

    # Clone DiffSinger if not present
    if not os.path.exists("DiffSinger"):
        subprocess.check_call(["git", "clone", "https://github.com/openvpi/DiffSinger.git"])
    
    os.chdir("DiffSinger")

    # Save lyrics
    with open("lyrics.txt", "w", encoding="utf-8") as f:
        f.write(lyrics)

    # Run DiffSinger inference (requires pretrained model in 'checkpoints')
    cmd = [
        "python", "inference.py",
        "--model", "checkpoints/singing_model.pth",
        "--config", "configs/config.yaml",
        "--midi", midi_path,
        "--lyrics", "../lyrics.txt",
        "--output", "../singing.wav"
    ]
    subprocess.check_call(cmd)

    os.chdir("..")

    # Step 3: Mix with beat if provided
    singing = AudioSegment.from_wav("singing.wav")
    if beat_file and os.path.exists(beat_file):
        beat = AudioSegment.from_file(beat_file)
        beat = beat[:len(singing)]  # match length
        final_mix = beat.overlay(singing)
    else:
        final_mix = singing

    final_mix.export(output_file, format="wav")
    print(f"✅ Final song saved as {output_file}")

# Example usage
if __name__ == "__main__":
    lyrics = "Shining bright, the stars align, guiding dreams through the night."
    bpm = 100
    beat_path = "drum_loop.wav"  # Optional beat file
    synthesize_singing(lyrics, bpm, beat_path)
