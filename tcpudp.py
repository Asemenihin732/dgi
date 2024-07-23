import socket
import time
from tkinter import messagebox
import tcpclient as ct

def reciever():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 33333)
    sock.bind(server_address)

    # Открываем файл для записи
    with open('received_file1.wav', 'wb') as f:
        while True:
            data, addr = sock.recvfrom(1024)
            print(data)
            if not data:
                break
            f.write(data)

    print("Файл успешно получен.")
    
def show_message(label ="", text = ""):
    messagebox.showinfo(label, text)    

def transmitter():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with open('test.wav', 'rb') as f:
        while True:
            bytes_read = f.read(64)
            if not bytes_read:
                break
            sock.sendto(bytes_read, ('localhost', 33333))
            time.sleep(0.01)

    print("Файл успешно отправлен.")
    
def transmit_file(client_socket, addr = "127.0.0.1", host = 33333, filepath=""):
    print("111")
    stop_byte = b'\x03\x04\x05\x06'
    with open(filepath, 'rb') as f:
        while True:
            bytes_read = f.read(1024)
            print(bytes_read)
            if not bytes_read:
                break
            client_socket.sendto(bytes_read, (addr, host))
            time.sleep(0.01)
    client_socket.send(stop_byte)
    print(stop_byte)

    print("Файл успешно отправлен.")
    
def start_server(host, port, path):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    show_message("TCP INFO", f"Listening on {host}:{port}")

    while True:
        print('True')
        client_sock, client_addr = server.accept()
        print('True3')
        print(client_sock)
        transmit_file(client_sock, filepath=path )
        print(client_addr)
        print("After transmitter2")
        print( f"Accepted connection from {client_addr}")
        print("After transmitter")
        break
    return client_sock
        

# start_server("127.0.0.1", 33333)

        