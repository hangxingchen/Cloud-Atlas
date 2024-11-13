# utils_tts.py
# Text-to-Speech (TTS)

print('Importing TTS module')

import os
import appbuilder
from API_KEY import *
import pyaudio
import wave

tts_ab = appbuilder.TTS()

def tts(TEXT='Welcome to Umbrella Corporation', tts_wav_path='temp/tts.wav'):
    '''
    Text-to-Speech (TTS) synthesis, generating a wav audio file
    '''
    inp = appbuilder.Message(content={"text": TEXT})
    out = tts_ab.run(inp, model="paddlespeech-tts", audio_type="wav")
    # out = tts_ab.run(inp, audio_type="wav")
    with open(tts_wav_path, "wb") as f:
        f.write(out.content["audio_binary"])
    # print("TTS synthesis completed, exported wav audio file to: {}".format(tts_wav_path))

def play_wav(wav_file='asset/welcome.wav'):
    '''
    Play wav audio file
    '''
    prompt = 'aplay -t wav {} -q'.format(wav_file)
    os.system(prompt)

# def play_wav(wav_file='temp/tts.wav'):
#     '''
#     Play wav file
#     '''
#     wf = wave.open(wav_file, 'rb')

#     # Instantiate PyAudio
#     p = pyaudio.PyAudio()

#     # Open audio stream
#     stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                     channels=wf.getnchannels(),
#                     rate=wf.getframerate(),
#                     output=True)

#     chunk_size = 1024
#     # Read audio data
#     data = wf.readframes(chunk_size)

#     # Play audio
#     while data != b'':
#         stream.write(data)
#         data = wf.readframes(chunk_size)

#     # Stop stream, close stream and PyAudio
#     stream.stop_stream()
#     stream.close()
#     p.terminate()
