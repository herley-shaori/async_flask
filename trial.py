import subprocess
import math

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return math.ceil(float(result.stdout))

panjangnya = get_length('static/video/video.mp4')
print('Panjang video: ', panjangnya)