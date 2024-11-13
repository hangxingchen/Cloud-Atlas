# sound_check.py
# Quick check of all voice-related features: microphone, recording, speaker playback, speech recognition, and text-to-speech synthesis

from utils_asr import *             # Recording and Speech Recognition
from utils_tts import *             # Text-to-Speech Module
print("Starting 5 seconds of recording")
record(DURATION=5)   # Start recording

print("Playing the recorded audio")
play_wav('temp/speech_record.wav')

speech_result = speech_recognition()
print("Starting text-to-speech synthesis")
tts(speech_result)

print("Playing the synthesized speech audio")
play_wav('temp/tts.wav')
