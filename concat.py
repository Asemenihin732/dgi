from pydub import AudioSegment
import wave
import contextlib
import time


    
def concaten(fileName, ms):
    with contextlib.closing(wave.open(fileName,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate) * 1000
        t1 = 0
        for i in range(0, round(duration/ms)):
        #Works in milliseconds
            t2 = t1+ms
            newAudio = AudioSegment.from_wav(fileName)
            newAudio = newAudio[t1:t2]
            newAudio.export('sound\part_' + str(i+1) + fileName.split("/")[-1], format="wav")
            t1+=ms


                          
# concaten(fname, 1000)