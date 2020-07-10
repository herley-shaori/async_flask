"""
Demo Flask application to test the operation of Flask with socket.io

Aim is to create a webpage that is constantly updated with random numbers from a background python process.

30th May 2014

===================

Updated 13th April 2018

+ Upgraded code to Python 3
+ Used Python3 SocketIO implementation
+ Updated CDN Javascript and CSS sources

"""




# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
import os
import pandas as pd

__author__ = 'slynn|herley'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

def randomNumberGenerator():
    kondisi = None
    # Jumlah frame minimal dengan keterangan_data.csv (berisi keterangan kelas setiap citra).
    jumlah_frame_minimal = 11
    indeks_gambar_sekarang = 0
    
    angka = None
    while not thread_stop_event.isSet():
        ada_gambar = False
        konten = None
        alamat_gambar = ''

        # Pembaruan video.
        if(angka == 2):
            socketio.emit('newnumber', {'number': angka}, namespace='/test')
            print('Script pembersih telah dijalankan: ', angka)

        # Periksa jumlah berkas dalam satu folder. Diminta minimal ada 10 frame untuk melakukan simulasi. Keterangan ini deprecated, akan dihapus.
        img_folder_path = 'static/images'
        dirListing = os.listdir(img_folder_path)

        if(len(dirListing) >= jumlah_frame_minimal):
            keterangan = pd.read_csv('static/images/keterangan_data.csv')
            if(keterangan.shape[0] == (len(dirListing) - 1)):

                indeks_gambar_sekarang+=1
                # Normalisasi indeks_gambar_sekarang dan hapus semua berkas dalam direktori.
                if(indeks_gambar_sekarang == (jumlah_frame_minimal-1)):
                    # indeks_gambar_sekarang = 0
                    angka = 2
                else:
                    if(indeks_gambar_sekarang < 10):
                        kelas = keterangan['kelas']
                        print('Indeks Gambar Sekarang: ', indeks_gambar_sekarang)
                        kelas_gambar = kelas[indeks_gambar_sekarang]
                        if(kelas_gambar == 1):
                            kondisi = True
                        else:
                            kondisi = False

                        if(kondisi):
                            angka = 1
                        else:
                            angka = 0

                        with open('data/text/teks.txt') as f:
                            konten = f.readlines()
                        # Buka untuk uji emisi angka.
                        # number = round(random()*10, 3)
                        socketio.emit('newnumber', {'number': angka}, namespace='/test')

                        if(kondisi):
                            socketio.sleep(4)
                        else:
                            socketio.sleep(1)

            else:
                print("Jumlah label citra: ", keterangan.shape[0], "tidak sama dengan jumlah data citra pada direktori: ", len(dirListing))
                print('Menunggu pembaruan citra...')
        else:
            print('Menunggu frame tambahan setiap 1 detik sekali...')
            print('Menunggu', (jumlah_frame_minimal - len(dirListing)), 'frame lagi.')
            print('-----------------------------------------------------------------')
            socketio.sleep(1)

@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(randomNumberGenerator)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
