import os
from moviepy.editor import ImageClip, AudioFileClip, TextClip, vfx, CompositeVideoClip
from pedalboard import Pedalboard, Reverb
import math
import subprocess
import soundfile

title = input("Title:")

print("Importing Audio And Image")
image = ImageClip("image.jpg")
audio = AudioFileClip("audio.mp3")

# convert mp3 to wav file
audio_file = 'audio.wav'

subprocess.call(['ffmpeg', '-i', 'audio.mp3',
                 audio_file])

# Import wav file
print('Importing audio...')
audio, sample_rate = soundfile.read(audio_file)

# Slow audio
print('Slowing audio...')
sample_rate -= math.trunc(sample_rate*0.09)

# Add reverb
print('Adding reverb...')
board = Pedalboard([Reverb(
    room_size=0.75,
    damping=0.5,
    wet_level=0.08,
    dry_level=0.2
    )])

# Add effects
effected = board(audio, sample_rate)

# Export audio
print('Exporting audio...')
soundfile.write("output.wav", effected, sample_rate)

audio_edited = AudioFileClip("output.wav")

# Adding title and artist
duration = 10
title = TextClip(title, font = 'font/brush.ttf', fontsize = 190, color='white')
title = title.set_duration(duration).set_start(t=5)


print('Generating Video')

screensize = (1920,1080)
video_file = image.set_audio(audio_edited)
video_file = CompositeVideoClip([video_file, title.set_position(('center'))], size=screensize)
video_file.duration = audio_edited.duration
video_file.write_videofile("Result[Slowed+Reverb].mp4", fps=1, codec='libx264')

os.remove('audio.wav')
os.remove('output.wav')
