# utils_asr.py
# Recording + Speech Recognition

print('hi DrHANG')

import pyaudio
import wave
import numpy as np
import os
import sys
from API_KEY import *
import appbuilder_sdk as appbuilder

# Determine microphone index
import sounddevice as sd
print(sd.query_devices())

def record(MIC_INDEX=2, DURATION=5):
    '''
    Record audio using the microphone. Use the "arecord -l" command to get the microphone ID.
    DURATION: Recording duration in seconds.
    '''
    print('Starting recording for {} seconds'.format(DURATION))
    os.system('sudo arecord -D "plughw:{}" -f dat -c 1 -r 16000 -d {} temp/speech_record.wav'.format(MIC_INDEX, DURATION))
    print('Recording finished')

def record_auto(MIC_INDEX=2):
    '''
    Start recording using the microphone and save to 'temp/speech_record.wav'.
    Recording starts automatically when the volume exceeds the threshold and stops after a period of low volume.
    MIC_INDEX: Microphone device index.
    '''
    
    CHUNK = 1024               # Sampling width
    RATE = 16000               # Sampling rate
    
    QUIET_DB = 2000            # Decibel threshold; starts recording when exceeded, stops otherwise
    delay_time = 1             # Time (in seconds) to stop recording after volume falls below the threshold
    
    FORMAT = pyaudio.paInt16
    CHANNELS = 1 if sys.platform == 'darwin' else 2 # Number of channels
    
    # Initialize recording
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=MIC_INDEX
                   )
    
    frames = []             # All audio frames
    
    flag = False            # Indicates if recording has started
    quiet_flag = False      # Indicates if the volume is below the threshold
    
    temp_time = 0           # Current frame index
    last_ok_time = 0        # Last frame with volume above the threshold
    START_TIME = 0          # Start frame index of recording
    END_TIME = 0            # End frame index of recording
    
    print('You can start speaking now!')
    
    while True:
        
        # Get the current chunk of audio data
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
        # Get the volume level of the current chunk
        temp_volume = np.max(np.frombuffer(data, dtype=np.short))
        
        if temp_volume > QUIET_DB and flag == False:
            print("Volume exceeded threshold, starting recording")
            flag = True
            START_TIME = temp_time
            last_ok_time = temp_time
    
        if flag:  # Various cases during recording
    
            if temp_volume < QUIET_DB and quiet_flag == False:
                print("Recording in progress, volume below threshold")
                quiet_flag = True
                last_ok_time = temp_time
                
            if temp_volume > QUIET_DB:
                # Volume is above the threshold, continue recording
                quiet_flag = False
                last_ok_time = temp_time
    
            if temp_time > last_ok_time + delay_time * 15 and quiet_flag == True:
                print("Volume below threshold for {:.2f} seconds, checking current volume".format(delay_time))
                if quiet_flag and temp_volume < QUIET_DB:
                    print("Volume still below threshold, stopping recording")
                    END_TIME = temp_time
                    break
                else:
                    print("Volume above threshold again, continuing recording")
                    quiet_flag = False
                    last_ok_time = temp_time
                    
        temp_time += 1
        if temp_time > 150:  # Exit if timeout occurs
            END_TIME = temp_time
            print('Timeout, stopping recording')
            break
    
    # Stop recording
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Export the audio as a wav file
    output_path = 'temp/speech_record.wav'
    wf = wave.open(output_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames[START_TIME-2:END_TIME]))
    wf.close()
    print('Audio saved to', output_path)

# Import AppBuilder SDK for ASR
import appbuilder
# Set the API token
os.environ["APPBUILDER_TOKEN"] = APPBUILDER_TOKEN
asr = appbuilder.ASR()  # Initialize ASR component

def speech_recognition(audio_path='temp/speech_record.wav'):
    '''
    AppBuilder-SDK Speech Recognition Component
    '''
    print('Starting speech recognition')
    # Load the wav audio file
    with wave.open(audio_path, 'rb') as wav_file:
        
        # Get basic information about the audio file
        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        framerate = wav_file.getframerate()
        num_frames = wav_file.getnframes()
        
        # Get the audio data
        frames = wav_file.readframes(num_frames)
        
    # Send a request to the ASR API
    content_data = {"audio_format": "wav", "raw_audio": frames, "rate": 16000}
    message = appbuilder.Message(content_data)
    speech_result = asr.run(message).content['result'][0]
    print('Speech recognition result:', speech_result)
    return speech_result
