import sounddevice as sd
import whisper
import numpy as np
import subprocess
from datetime import datetime

SAMPLE_RATE = 16000
RECORD_SECONDS = 5


def speak(text):
    print("🐺 WOLF:")
    print(text)
    print("🔊 Speaking...")

    subprocess.Popen(["say", text])


def process_command(text):
    text = text.lower().strip()

    print("")
    print("🧠 COMMAND:")
    print(text)
    print("")

    # TIME
    if "time" in text or "hora" in text:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")
        return

    # DATE
    if "date" in text or "fecha" in text:
        current_date = datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {current_date}")
        return

    # HELLO
    if "hello" in text or "hi" in text or "hola" in text:
        speak("Hello. I am WOLF.")
        return

    # STATUS
    if "status" in text:
        speak("All WOLF systems are operational.")
        return

    # WHO ARE YOU
    if "who are you" in text or "what are you" in text:
        speak("I am WOLF, the artificial intelligence of WOLF OS.")
        return

    # UNKNOWN COMMAND
    speak("I heard you, but I do not know that command yet.")


print("🐺 WOLF VOICE")
print("")
print("Loading Whisper AI...")
print("")

model = whisper.load_model("base")

print("✅ Whisper ready!")
print("🎤 Microphone detected.")
print("")
print("Say:")
print('"WOLF, what time is it?"')
print("")

try:

    recording = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    print("")
    print("🧠 WOLF is thinking...")

    audio = recording.flatten().astype(np.float32) / 32768.0

    result = model.transcribe(
        audio,
        language="en",
        fp16=False
    )

    text = result["text"].strip()

    print("")

    if text:
        print("🎤 WOLF HEARD:")
        print(text)

        process_command(text)

    else:
        print("❓ WOLF didn't hear anything.")

except Exception as error:

    print("")
    print("❌ ERROR:")
    print(error)
