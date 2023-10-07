import pyaudio
import numpy as np
import wave

def baby_voice_modulator(output_path, pitch_shift=1.3):
    CHUNK = 1024
    RATE = 44100

    p = pyaudio.PyAudio()

    input_stream = p.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=RATE,
                          input=True,
                          frames_per_buffer=CHUNK)

    print("Baby Voice Modulator is running. Press Ctrl+C to stop.")

    try:
        frames = []
        while True:
            data = input_stream.read(CHUNK)
            audio_data = np.frombuffer(data, dtype=np.int16)

            #Apply pitch shift to create a baby voice effect
            shifted_audio_data = np.interp(
                np.arange(0, len(audio_data), pitch_shift),
                np.arange(0, len(audio_data)),
                audio_data
            ).astype(np.int16)

            frames.append(shifted_audio_data.tobytes())

    except KeyboardInterrupt:
        print("Baby Voice Modulator stopped.")
        input_stream.stop_stream()
        input_stream.close()
        p.terminate()

        #Save the recorded audio to a WAV file
        with wave.open(output_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

if __name__ == "__main__":
    output_file_path = "C:\\Users\\GSori\\OneDrive\\Documents\\4thYear\\DSPA\\markName_output.wav"
    baby_voice_modulator(output_file_path, pitch_shift=1.3)