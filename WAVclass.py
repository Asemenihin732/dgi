import struct
import librosa.display
import matplotlib.pyplot as plt

class wavfile():

    def __init__(self, chunkId, chunkSize, formatName,  subchunk1Id,
                subchunk1Size, audioFormat, numChannels, sampleRate, byteRate,
                blockAlign, bitsPerSample, subchunk2Id, subchunk2Size, pureAdcData):
        self.chunkId = chunkId
        self.chunkSize = chunkSize
        self.formatName = formatName
        self.pureAdcData = pureAdcData
        self.subchunk1Id = subchunk1Id
        self.subchunk1Size = subchunk1Size
        self.audioFormat = audioFormat
        self.numChannels = numChannels
        self.sampleRate = sampleRate
        self.byteRate = byteRate
        self.blockAlign = blockAlign
        self.bitsPerSample = bitsPerSample
        self.subchunk2Id = subchunk2Id
        self.subchunk2Size = subchunk2Size

    def printData(self):
        print("Your .WAV file consist of next data:\n" + str(self.chunkId) +"\n"+ str(*self.chunkSize) +"\n"+ 
             str(self.formatName) +"\n"+ str(self.subchunk1Id) +"\n"+ str(*self.subchunk1Size)+"\n" +
             str(*self.audioFormat)+"\n" + str(*self.numChannels)+"\n"+ str(*self.sampleRate)+"\n" + str(*self.byteRate)+"\n" +
             str(*self.blockAlign)+"\n" + str(*self.bitsPerSample)+"\n" + str(self.subchunk2Id)+"\n" + str(*self.subchunk2Size)+'\n' + str(self.pureAdcData))
        
    def printDataWithoutPureADC(self):
        result = ("Your .WAV file consist of next data:\n" + str(self.chunkId) +"\n"+ str(*self.chunkSize) +"\n"+ 
             str(self.formatName) +"\n"+ str(self.subchunk1Id) +"\n"+ str(*self.subchunk1Size)+"\n" +
             str(*self.audioFormat)+"\n" + str(*self.numChannels)+"\n"+ str(*self.sampleRate)+"\n" + str(*self.byteRate)+"\n" +
             str(*self.blockAlign)+"\n" + str(*self.bitsPerSample)+"\n" + str(self.subchunk2Id)+"\n" + str(*self.subchunk2Size))
        return result
    
def openWav(wav_File):
    with open(str(wav_File), "rb") as file:
        data = file.read()
        
    chunkId = data[0:4].decode()
    chunkSize = struct.unpack_from('i', data[4:8])
    formatName = data[8:12].decode()
    subchunk1Id = data[12:16].decode()
    subchunk1Size = struct.unpack_from('i', data[16:20])
    audioFormat = struct.unpack_from('h', data, offset=20)
    numChannels = struct.unpack_from('h', data, offset=22)
    sampleRate = struct.unpack_from('i', data, offset=24)
    byteRate = struct.unpack_from('i', data, offset=28)
    blockAlign = struct.unpack_from('H', data, offset=32)
    bitsPerSample = struct.unpack_from('h', data, offset=34)
    subchunk2Id = data[36:40].decode()
    subchunk2Size = struct.unpack_from('i', data, offset=40)
    pureAdcData =[a for a in struct.iter_unpack("H",data[44:])]
    MyWav = wavfile(chunkId, chunkSize, formatName, subchunk1Id, subchunk1Size, audioFormat,
    numChannels, sampleRate, byteRate, blockAlign,bitsPerSample, subchunk2Id, subchunk2Size, pureAdcData)
    
    return MyWav.printDataWithoutPureADC()

def spectr(wav_file):
    y, sr = librosa.load(str(wav_file))
    X = librosa.stft(y)
    Xdb = librosa.amplitude_to_db(abs(X))
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
    #librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='log') # Логарифмический масштаб по Y
    plt.colorbar()
    plt.show()