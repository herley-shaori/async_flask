

# --------------------------------------------------------------------------
import os
import cv2
import pandas as pd

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
		else:
			# Jika frame yang diputar bukan kelas tujuan, maka cukup menambah satu frame pada video.
			for x in range(0, 1):
				video.write(resized)
	video.release()

	os.system('ffmpeg -i video.avi luaran.mp4 -y')
else:
	print("Panjang kelas dan jumlah gambar tidak sama.")

