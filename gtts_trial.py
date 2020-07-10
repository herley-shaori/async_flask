# Memasukkan suara semu.

from pydub import AudioSegment

suara = AudioSegment.from_mp3("halo.mp3")
# durasi senyap.
detik = 0.5
silence = AudioSegment.silent(duration=(detik*1000))
gabungan = suara + silence + suara + silence + suara + silence + suara + silence + suara

gabungan.export("gabungan.mp3", format="mp3")

# from gtts import gTTS
# tts = gTTS('hello I am your new customer', lang='en')
# tts.save('hello.mp3')

# avconv -v debug -i gabungan.mp3 -i luaran.mp4 -c:a libmp3lame -qscale 20 -shortest video_jadi.mp4
# ffmpeg -i luaran.mp4 -i halo.mp3 -c:v copy -c:a aac video_jadi.mp4