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

# Keterangan indeks angka:
# 0 --> kelas 0.
# 1 --> kelas 1.
# 2 --> aplikasi berhenti.
# 3 --> menunggu video baru.

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
    jumlah_frame_minimal = 10
    frame_sekarang = 0
    
    angka = None
    while not thread_stop_event.isSet():
        ada_gambar = False
        konten = None

        # Pembaruan video.
        if(angka == 2):
            socketio.emit('newnumber', {'number': angka}, namespace='/test')
            print('Script pembersih telah dijalankan: ', angka)
            # Kembalikan pemutaran video jika video baru sudah ada.
            dirListing = os.listdir(video_folder_path)
            if(dirListing > 0):
                angka = -1
                frame_sekarang = 0


        # Direktori Video.
        video_folder_path = 'static/video' 
        dirListing = os.listdir(video_folder_path)
        if(len(dirListing) > 0):
            keterangan = pd.read_csv('static/label/keterangan_data.csv')
            frame_sekarang+=1
            # Normalisasi frame_sekarang dan hapus semua berkas dalam direktori.
            if(frame_sekarang == (jumlah_frame_minimal)):
                angka = 2
            else:
                if(frame_sekarang < jumlah_frame_minimal):
                    kelas = keterangan['kelas']
                    kelas_gambar = kelas[frame_sekarang]
                    if(kelas_gambar == 1):
                        kondisi = True
                    else:
                        kondisi = False

                    if(kondisi):
                        angka = 1
                    else:
                        angka = 0

                    # Buka untuk uji emisi angka.
                    # number = round(random()*10, 3)
                    socketio.emit('newnumber', {'number': angka}, namespace='/test')
                    if(kondisi):
                        socketio.sleep(4)
                    else:
                        socketio.sleep(1)
        else:
            print('Menunggu video baru...')
            angka = 3
            socketio.emit('newnumber', {'number': angka}, namespace='/test')
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
