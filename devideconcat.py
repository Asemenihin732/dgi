import wave
import struct
rate = None


def split_wav_into_chunks(wav_file, chunk_size_ms=10):
    global rate
    with wave.open(wav_file, 'rb') as f:
        frames = f.getnframes()
        rate = f.getframerate()
        chunk_size = int(rate * chunk_size_ms / 1000)
        # print(rate)
        chunks = []
        for i in range(0, frames, chunk_size):
            data = f.readframes(chunk_size)
            chunks.append(data)
        # print (chunks)
    return chunks
# здесь происходит преобразование данных из ваф файла в байты


# # for chunk in chunks:
# #     # print(chunk)
# #     # print('\n')
# def concat_wav(output_file)
# output_file = 'output_file3.wav'
# chunks = split_wav_into_chunks
# with wave.open(output_file, 'wb') as f:
#     f.setnchannels(1)
#     f.setsampwidth(4)
#     f.setframerate(44100)

#     for chunk in chunks:
#         f.writeframes(chunk)