import WAVclass as wv
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
import ComPortClientMy as ec
from tkinter import messagebox
import socket
import tcpudp as tu
import tcpclient as tc
import concat as cct
import serial.tools.list_ports



# def open_number_window():
#     number_window = tk.Toplevel(root)
#     number_window.title("Введите число")

#     # Метка для ввода числа
#     number_label = tk.Label(number_window, text="Введите число:")
#     number_label.grid(row=0, column=0)

#     # Спинбокс для ввода числа
#     number_spinbox = tk.Spinbox(number_window, from_=0, to=100)
#     number_spinbox.grid(row=0, column=1)

#     # Кнопка "Отмена"
#     cancel_button = tk.Button(number_window, text="Отмена", command=number_window.destroy)
#     cancel_button.grid(row=1, column=0)

#     # Кнопка "ОК"
#     ok_button = tk.Button(number_window, text="ОК", command=lambda: get_number(number_spinbox.get()))
#     ok_button.grid(row=1, column=1)

# def get_number(number):
#     print(f"Введено число: {number}")
#     number_window.destroy()


def create_dropdown(root, options, label_text, row , column):
        # Создаем метку
    label = tk.Label(root, text=label_text)
    label.grid(row=row, column=column)  
    
    selected_option = tk.StringVar(root)
    selected_option.set(options[0])  

    # Создаем выпадающий список
    dropdown = tk.OptionMenu(root, selected_option, *options)
    dropdown.grid(row=row, column=column+1)  # Используем grid вместо pack

    return selected_option


    


def openSpectr():
    global wavFile
    if wavFile is None:
        show_message("Файл еще не открыт")
        return
    wv.spectr(wavFile)

def transmitter():
    global wavFile
    global selected_connection
    global selected_com_port
    global selected_baud_rate
    if selected_connection.get() == "COM":
        if wavFile is None:
            show_message("Файл еще не открыт")
            return
        print("transmitter")
        print("reciever")
        print(int(selected_baud_rate.get()))
        print(selected_com_port.get())
        ec.send_file(wavFile, stop_byte, selected_com_port.get(), int(selected_baud_rate.get()) )
    elif selected_connection.get() == "TCP":
        show_message('TCP', "TCP передатчик")
        if wavFile is None:
            show_message("Файл еще не открыт")
            return
        tu.start_server("127.0.0.1", 33333, wavFile)
        
            
    else:
        print("ghbg")
        
        
        
        

def show_message(label ="", text = ""):
    messagebox.showinfo(label, text)

def reciever():
    if selected_connection.get() == "COM":
        global selected_com_port
        global selected_baud_rate
        print("reciever")
        print(int(selected_baud_rate.get()))
        print(selected_com_port.get())
        ec.receive_file(selected_com_port.get(), int(selected_baud_rate.get()))
    elif selected_connection.get() == "TCP":
        tc.receive_file("127.0.0.1", 33333)
    else:
        print("ghbg")
    
    
def concatenate():
    if number_entry is not None:
        if wavFile is None:
            show_message("Файл еще не открыт")
            return
        print(int(number_entry.get()))
        cct.concaten(wavFile, int(number_entry.get()))
        # Продолжайте использовать значение в вашем коде
    else:
        print("number_entry равен None")
    
def on_spinbox_change(*args):
    new_value = spinbox_var.get()
    print(f"Новое значение: {new_value}")

def main():    
    root = Tk()
    stop_byte = b'\x03\x04\x05\x06'
    wavFile = None
    global selected_com_port
    global selected_baud_rate
    global selected_connection
    global ms
    global number_entry
    def openFile():
        global wavFile
        wavFile = filedialog.askopenfilename().format("WAV")
        if wavFile != "":
            result = wv.openWav(wavFile)
            result_label.config(text=result) 
            root.update()

    spinbox_var = tk.IntVar()
    spinbox_var.trace("w", on_spinbox_change)
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Button(frm, text="Search", command=openFile).grid(column=1, row=0)
    ttk.Button(frm, text="Spectr", command=openSpectr).grid(column=2, row=0)
    ttk.Button(frm, text="Transmit", command=transmitter).grid(column=1, row=1)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=2, row=1)
    ttk.Button(frm, text="Recieve", command=reciever).grid(column=1, row=2)
    ttk.Button(frm, text="Concatenate", command=concatenate).grid(column=2, row=2)
    number_entry = ttk.Spinbox(frm,from_=10, to=6000, increment=10 )
    number_entry.grid(column=1, row=3)
    ttk.Label(frm,text="Enter ms to concat").grid(column=2,row=3)
    # ttk.Button(frm, text="Start Server", command=serv.start_server("127.0.0.1", 5000)).grid(column=1, row=2)
    # ttk.Button(frm, text="Number", command=open_number_window).grid(column=2, row=2)
    ports = serial.tools.list_ports.comports()
    com_ports = []
    for port in ports:
        print(port.device)
        com_ports.append(port.device)
    selected_com_port = create_dropdown(root, com_ports, "Выберите COM порт:",1,1)
    baud_rates = ["9600", "14400", "19200", "38400", "57600", "115200"]
    selected_baud_rate = create_dropdown(root, baud_rates, "Выберите скорость передачи:",2,1)
    con_type = ["COM", "TCP"]
    
    selected_connection = create_dropdown(root, con_type, "Выберите тип соединения:",3,1)
    result_label = ttk.Label(frm, text="")
    result_label.grid(column=1, row=4, columnspan=2)
    root.mainloop()


number_entry = None
stop_byte = b'\x03\x04\x05\x06'
wavFile = None
ms = None
spinbox_var=0
selected_com_port = None
selected_baud_rate = None
selected_connection = None
main()





