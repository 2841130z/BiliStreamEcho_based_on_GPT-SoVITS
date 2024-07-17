import io
import os
import subprocess

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from pygame import mixer

from scipy.io.wavfile import write


def rm_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print(f"{file_path} not exists")
    except Exception as e:
        print(str(e))


def ndarray_to_bytes(audio):
    byte_io = io.BytesIO(bytes())
    write(byte_io, 22050, audio)
    output = byte_io.read()
    return output


def save_to_wav(res_path, audio):
    write(res_path, 22050, audio)
    return res_path


def wav_to_mp3(wav_file):
    result = wav_file.replace(".wav", ".mp3")
    subprocess.run(args=f"ffmpeg -y -i {wav_file} {result}", shell=True)
    return result


def playsound_via_pygame(audio):
    mixer.init()
    # mixer.music.set_volume(0.75)  # 音量控制 默认 1.0
    if isinstance(audio, bytes):
        mixer.music.load(io.BytesIO(audio))
    else:
        audio = save_to_wav("ttscache/tmp.wav", audio)
        mixer.music.load(audio)
    mixer.music.play()
    while mixer.music.get_busy():
        pass
    mixer.music.unload()
    mixer.quit()
