import os
from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, TextClip, CompositeVideoClip, vfx
from moviepy.video.tools.subtitles import SubtitlesClip
from pedalboard import Pedalboard, Reverb
from math import trunc

import soundfile
import subprocess

title = input("Title:")
artist = input("Artist:")

print("Importing Audio And Image")
image = ImageClip("image.jpg")
audio = AudioFileClip("audio.mp3")


duration = 10
title = TextClip(title, font = 'font/brush.ttf', fontsize = 50, color='white')
title = title.set_position((50, 50)).set_duration(duration).set_start(t=5)#.crossfadein(1.0).crossfadeout(1.0)
artist = TextClip(artist, font = 'font/brush.ttf', fontsize = 50, color='white')
artist = artist.set_position((50, 125)).set_duration(duration).set_start(t=5)#.crossfadein(1.0).crossfadeout(1.0)


generator = lambda txt: TextClip(txt, font='font/brush.ttf', fontsize=120, color='White')
subs = SubtitlesClip("sub.srt", generator)

screensize = (1920,1080)

image = image.set_position('center')
video = image.set_duration(audio.duration)
video = CompositeVideoClip([video.fx(vfx.colorx, 0.6), subs.set_position(('center'))], size=screensize)

slow_video = video.speedx(0.9)
slow_video.write_videofile("video.mp4", fps=1, codec='libx264')
slow_video = VideoFileClip("video.mp4")


audio_file = 'audio.wav'

# convert mp3 to wav file
subprocess.call(['ffmpeg', '-i', 'audio.mp3',
                 audio_file])

# Import audio file
print('Importing audio...')
audio, sample_rate = soundfile.read(audio_file)

# Slow audio
print('Slowing audio...')
sample_rate -= trunc(sample_rate*0.11)

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

print('Generating Video')
video_file = slow_video.set_audio(audio_edited)
video_file.duration = audio_edited.duration

video_file.write_videofile("Result[Slowed+Reverb].mp4")

#os.remove('sub.srt')
os.remove('audio.wav')
os.remove('output.wav')
os.remove('video.mp4')
