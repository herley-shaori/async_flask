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
from flask import Flask, render_template, url_for, copy_current_request_context, redirect
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

__author__ = 'slynn'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Watchdog global variable.
global jalanwd
jalanwd = False

def on_created(event):
    print(f"hey, {event.src_path} has been created!")
    return redirect('/indeksDua')

def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")

def on_modified(event):
    print("hey buddy, {event.src_path} has been modified. Langsung ada efeknya.")


def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")

def jalankan_watchdog():
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    # The Observer.
    path = "."
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    # Start the observer.
    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()

@app.route('/indeksDua')
def duaIndex():
    return render_template('index.html', pesan='Pesan dari Thread')

@app.route('/')
def index():
    return render_template('index.html', pesan='Pesan dari Aplikasi Pusat')

if __name__ == '__main__':
    # Uncomment ketika aplikasi Flask telah berjalan.
    # jalankan_watchdog()
    app.run()
