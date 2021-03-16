import time
import numpy as np
import pyaudio
import music.config as config
import music.visualization as visualization

p = None
stream = None
frames_per_buffer = None


def start_stream():
    global p, stream, frames_per_buffer
    p = pyaudio.PyAudio()
    frames_per_buffer = int(config.MIC_RATE / config.FPS)
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=config.MIC_RATE,
                    input=True,
                    frames_per_buffer=frames_per_buffer)



def close_stream():
    global stream, p

    if p and stream:
        stream.stop_stream()
        stream.close()
        p.terminate()
        p = None
        stream = None


def update_stream():
    overflows = 0
    prev_ovf_time = time.time()

    try:
        y = np.fromstring(stream.read(frames_per_buffer, exception_on_overflow=False), dtype = np.int16)
        y = y.astype(np.float32)
        stream.read(stream.get_read_available(), exception_on_overflow=False)
        visualization.microphone_update(y)
    except IOError:
        overflows += 1
        if time.time() > prev_ovf_time + 1:
            prev_ovf_time = time.time()
            print('Audio buffer has overflowed {} times'.format(overflows))

