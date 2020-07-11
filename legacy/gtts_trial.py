# Memasukkan suara semu.

from pydub import AudioSegment

suara = AudioSegment.from_mp3("halo.mp3")
# durasi senyap.
detik = 0.5
silence = AudioSegment.silent(duration=(detik*1000))
gabungan = suara + silence + suara + silence + suara + silence + suara + silence + suara

silence.export("gabungan.mp3", format="mp3")
# ffmpeg -i luaran.mp4 -i halo.mp3 -c:v copy -c:a aac video_jadi.mp4