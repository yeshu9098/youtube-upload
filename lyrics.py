import pylrc

print('Importing Lyrics')
lrc_file = open("lyric.lrc")
lrc_string = ''.join(lrc_file.readlines())
lrc_file.close()

# convert lrc to srt string
print('Converting Lyrics')
subs = pylrc.parse(lrc_string)
srt = subs.toSRT()

file = open('sub.srt', 'w')
file.write(srt)
file.close()