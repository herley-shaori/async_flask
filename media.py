import os
import cv2
import pandas as pd
from pydub import AudioSegment

dir_path = 'static/images'
ext = '.JPG'
output = 'video.avi'
shape = 300, 300
# Makin tinggi nilai fps, makin cepat pergantian gambar.
fps = 1
# Makin tinggi nilai normal_frame_appender, makin lambat citra berganti.
normal_frame_appender = 4

data = pd.read_csv(dir_path+'/keterangan_data.csv')
data.sort_values('citra')
image_list = data['citra']
class_list = data['kelas']
# Pelanggaran didefinisikan pada kelas 1.
kelas_pelanggaran = 1

# Suara.
suara = AudioSegment.from_mp3("static/audio/halo.mp3")
detik = 0.5
senyap = AudioSegment.silent(duration=(detik*1000))
suara_gabungan = None

if(len(image_list) == len(class_list)):
	fourcc = cv2.VideoWriter_fourcc(*'DIVX')
	video = cv2.VideoWriter(output, fourcc, fps, shape)

	for index in range(0,len(image_list)):
		kelas_saat_ini = class_list[index]
		image = image_list[index]
		image = str(image)+'.JPG'
		image_path = os.path.join(dir_path, image)
		image = cv2.imread(image_path)
		resized=cv2.resize(image,shape)
		if(kelas_saat_ini == kelas_pelanggaran):
			# Frame sama dengan 4 detik menyesuaikan dengan panjang halo.mp3
			for x in range(0, normal_frame_appender):
				video.write(resized)
			if(suara_gabungan is None):
				suara_gabungan = suara
			else:
				suara_gabungan+=suara
		else:
			# Jika frame yang diputar bukan kelas tujuan, maka cukup menambah satu frame pada video.
			for x in range(0, 1):
				video.write(resized)
			if(suara is None):
				suara_gabungan=senyap
			else:
				suara_gabungan+=senyap

	# Luaran video.
	video.release()
	suara_gabungan.export("suara_gabungan.mp3", format="mp3")
	os.system('ffmpeg -i video.avi video.mp4 -y')
	os.system('ffmpeg -i video.mp4 -i suara_gabungan.mp3 -c:v copy -c:a aac video_jadi.mp4 -y')
	os.remove("video.mp4")
	os.remove("video.avi")
	os.remove("suara_gabungan.mp3")
	os.rename('video_jadi.mp4', 'static/video/video.mp4')
else:
	print("Panjang kelas dan jumlah gambar tidak sama.")