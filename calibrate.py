import os
import pyaudio
from p2fa import align

import wave

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 6
TRANSCRIPT_FILENAME = "assets/transcription.txt"
CALIBRATION_FILENAME = "assets/calibrate.wav"

def record(length=RECORD_SECONDS):
    with open(TRANSCRIPT_FILENAME) as f:
        prompt = f.read()
    output_file=CALIBRATION_FILENAME

    if prompt is not None:
        print("Please read:", prompt)

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print("recording...")
    frames = []
    for i in range(0, int(RATE / CHUNK * length)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")

    if output_file is not None:
        stream.stop_stream()
        stream.close()
        audio.terminate()

        waveFile = wave.open(CALIBRATION_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
