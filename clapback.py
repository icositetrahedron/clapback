import argparse
import math
import os
import struct
import sys
import time
import pyaudio
from p2fa import align
from pydub import AudioSegment
from pydub.playback import play
import wave
import calibrate

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
TRANSCRIPT_FILENAME = "assets/transcription.txt"
CALIBRATION_FILENAME = "assets/backup_calibrate.wav"
CALIBRATION_ON=True

# https://stackoverflow.com/questions/25868428/pyaudio-how-to-check-volume
def rms(data):
    count = len(data)//2
    format = "%dh"%(count)
    shorts = struct.unpack( format, data )
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0/32768)
        sum_squares += n*n
    return math.sqrt( sum_squares / count )

def dbfs(data):
    return 20*math.log10(rms(data) * math.sqrt(2))

def mlf_to_ms(ns):
    return (ns/10000 + 0.0125)*(11000/11.025)

def get_vol_at_timestamp(audio, start, end):
    audio_chunk = audio[mlf_to_ms(start):mlf_to_ms(end)]
    return audio_chunk.dBFS

def record(dbfs_for_clap, time_for_clap, length=RECORD_SECONDS):
    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print("recording...")
    frames = []
    clap = AudioSegment.from_file("assets/clap.wav")
    def play_clap():
        play(clap)
    starttime = None
    for i in range(0, int(RATE / CHUNK * length)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        if dbfs(data) >= dbfs_for_clap:
            if starttime is None:
                starttime = time.time_ns()
                play_clap()
            else:
                time_elapsed = (time.time_ns() - starttime)/50
                if time_elapsed >= time_for_clap:
                    starttime = time.time_ns()
                    play_clap()

        frames.append(data)
    print("finished recording")


parser = argparse.ArgumentParser(description='Clap as you talk.')
parser.add_argument('-l', '--length', metavar='N', type=int, default=10, help='how many seconds to record for clapping')
parser.add_argument('-c', '--recalibrate', action='store_true', help='re-record calibration file')
parser.add_argument('-d', '--default_calibration', action='store_true', help='use default calibration file')

args = parser.parse_args()
if args.recalibrate:
    calibrate.record()
if os.path.isfile("assets/calibrate.wav") and not args.default_calibration:
    CALIBRATION_FILENAME="assets/calibrate.wav"
    phoneme_alignments, word_alignments = align.align(CALIBRATION_FILENAME, TRANSCRIPT_FILENAME)

    audio = AudioSegment.from_wav(CALIBRATION_FILENAME)

    word_dbfs = []
    word_midpoints = []

    for word, time_start, time_end in word_alignments:
        if word != "sp":
            word_dbfs.append(get_vol_at_timestamp(audio,time_start,time_end))
            word_midpoints.append((time_end+time_start)/2)

    max_dbfs = max(word_dbfs)
    min_time = mlf_to_ms(min([word_midpoints[i+1]-word_midpoints[i] for i in range(len(word_midpoints)-1)]))*10**6
else:
    CALIBRATION_FILENAME="assets/backup_calibrate.wav"
    max_dbfs=-16.576273313948487
    min_time=12489573.788699154

record(dbfs_for_clap=max_dbfs, time_for_clap=min_time, length=args.length)
