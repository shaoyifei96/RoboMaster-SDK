from pathlib import Path
from openai import OpenAI
from pydub import AudioSegment

def generate_speech(text, output_path="temp_speech.wav"):
    client = OpenAI()
    
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="onyx",
        input=text,
        instructions="Speak in a formal, professional British accent with precise enunciation",
        response_format="wav",
    )
    
    # Save the initial WAV file
    response.stream_to_file(output_path)

    # Convert the audio to the correct format using pydub
    audio = AudioSegment.from_wav(output_path)
    audio = audio.set_frame_rate(48000)  # Set to 48kHz
    audio = audio.set_channels(1)        # Convert to mono
    audio = audio.set_sample_width(2)    # Set to 16-bit
    audio.export(output_path, format="wav")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        text = sys.argv[1]
        generate_speech(text)
