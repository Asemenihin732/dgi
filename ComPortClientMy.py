import serial
import time
import wave
from tkinter import filedialog
from tkinter import messagebox

from devideconcat import split_wav_into_chunks

def show_message(label ="", text = ""):
    messagebox.showinfo(label, text)
    
def send_file(file_path, stop_byte,  serial_port='COM1', baud_rate=9600): #тут раньше передавал файл целиком
    ser = serial.Serial(serial_port, baud_rate)
    with open(file_path, 'rb') as file:
        print('Начинаем передачу файла...')
        start_time = time.time()
        show_message("Внимание",f'Начинаем передачу файла...')
        while True:
            data = file.read(1024)
            if not data:
                break
            ser.write(data)
            time.sleep(0.01)
        print('Передача файла завершена.')
        elapsed_time = time.time() - start_time
        show_message("Внимание",f'Передача файла завершена. Затраченное время: {elapsed_time} секунд  ')
        ser.write(stop_byte)
        
        
def get_samplewidth_from_wav(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        samplewidth = wav_file.getsampwidth()
        # print(samplewidth)
        return samplewidth
        
def receive_file( serial_port="COM2", baud_rate=9600): #тут раньше принимал файл целиком
    s=serial.Serial(serial_port,baud_rate)
    start_time = time.time()
    stop_byte = b'\x03\x04\x05\x06'
    file_path = filedialog.asksaveasfilename(defaultextension=".wav")
    with open(file_path, 'wb') as file:
            print('Начинаем прием файла...')
            show_message("Внимание", "Начало приема файла")
            while True:
                if s.in_waiting > 0:
                # Читаем данные из COM порта
                    data = s.read(s.in_waiting)
                    print(data)
                    file.write(data)
                    if stop_byte in data:
                        print("stop_byte") 
                        break
                    time.sleep(0.01)
            print('Прием файла завершен.')
            elapsed_time = time.time() - start_time
            print(f'Прием файла завершен. Затраченное время: {elapsed_time} секунд')
            show_message("Внимание",f'Прием файла завершен. Затраченное время: {elapsed_time} секунд')
            
    
def receive_file1( serial_port="COM2", baud_rate=9600):
    s=serial.Serial(serial_port,baud_rate)
    start_time = time.time()
    stop_byte = b'\x03\x04\x05\x06'
    st_count = 0
    file_path = filedialog.asksaveasfilename(defaultextension=".wav")
    with wave.open(file_path, 'wb') as file:
            print('Начинаем прием файла...')
            show_message("Внимание", "Начало приема файла")
            file.setnchannels(1)
            
            file.setframerate(44100)
            while True:
                if s.in_waiting > 0:
                # Читаем данные из COM порта
                    if st_count==0:
                        data = s.read(s.in_waiting)
                        print(int.from_bytes(data, "big"))
                        # file.setsampwidth(int.from_bytes(data, "big"))
                        
                        st_count+=1
                    
                    else:
                        if stop_byte in data:
                            print("stop_byte") 
                            break
                        file.writeframes(data)
                        time.sleep(0.01)
            print('Прием файла завершен.')
            elapsed_time = time.time() - start_time
            print(f'Прием файла завершен. Затраченное время: {elapsed_time} секунд')
            show_message("Внимание",f'Прием файла завершен. Затраченное время: {elapsed_time} секунд')
            
# def receive_file1(serial_port="COM2", baud_rate=9600):
#     s = serial.Serial(serial_port, baud_rate)
#     start_time = time.time()
#     stop_byte = b'\x03\x04\x05\x06'
#     file_path = filedialog.asksaveasfilename(defaultextension=".wav")
    
#     # Определение samplewidth на основе данных из файла
#     samplewidth = None
    
#     with wave.open(file_path, 'wb') as file:
#         print('Начинаем прием файла...')
#         show_message("Внимание", "Начало приема файла")
#         file.setnchannels(1)
#         file.setframerate(44100)
#         while True:
#             if s.in_waiting > 0:
#                 # Читаем данные из COM порта
#                 data = s.read(s.in_waiting)
#                 print(data)
                
#                 if stop_byte in data:
#                     print("stop_byte") 
#                     break
#                 if samplewidth is None:
#                     samplewidth += len(data)
#                     file.setsampwidth(samplewidth)
#                 # Определение samplewidth на основе первого пакета данных
                
                
#             file.writeframes(data)
#             time.sleep(0.01)
            
        
#     print('Прием файла завершен.')
#     elapsed_time = time.time() - start_time
#     print(f'Прием файла завершен. Затраченное время: {elapsed_time} секунд')
#     show_message("Внимание", f'Прием файла завершен. Затраченное время: {elapsed_time} секунд')            

def send_file1(file_path, stop_byte,  serial_port='COM1', baud_rate=9600):
    ser = serial.Serial(serial_port, baud_rate)
    smp_width = get_samplewidth_from_wav(file_path)
    # ser.write(smp_width)
    # # print(smp_width)
    # ser.write(stop_byte)
    chunks = split_wav_into_chunks(file_path, 1000)

    for chunk in chunks:
        ser.write(chunk)
        # print (chunk)
        
    show_message("Внимание", "Передача файла завершена")
    print('Передача файла завершена.')
    # elapsed_time = time.time() - start_time
    ser.write(stop_byte)