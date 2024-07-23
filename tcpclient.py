import socket
import time
import wave
from tkinter import messagebox
from tkinter import filedialog

def show_message(label ="", text = ""):
    messagebox.showinfo(label, text)    

def receive_file(server_address, server_port):
    try:
        # Создаем сокет
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_address, server_port))
        start_time = time.time()
        stop_byte = b'\x03\x04\x05\x06'
        file_path = filedialog.asksaveasfilename(defaultextension=".wav")
        with open(file_path, 'wb') as file:
            print('Начинаем прием файла...')
            while True:
                data = client_socket.recv(1024)  # Читаем данные из сокета
                if not data:
                    break
                file.write(data)
                if stop_byte in data:
                    print("stop_byte")
                    break
                time.sleep(0.01)
            print('Прием файла завершен.')
            elapsed_time = time.time() - start_time
            print(f'Затраченное время: {elapsed_time:.2f} секунд')
    except Exception as e:
        print(f"Ошибка при получении файла: {e}")
    finally:
        client_socket.close()



# Пример использования:
# if __name__ == "__main__":
#     server_ip = "127.0.0.1"  # Замените на IP-адрес сервера
#     server_port = 33333  # Замените на порт сервера
#     output_filename = 'received_file1.wav'  # Имя файла, в который будет сохранен полученный контент
#     receive_file(server_ip, server_port)
