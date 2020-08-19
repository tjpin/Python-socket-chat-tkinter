import socket
from tkinter import *
import tkinter
from threading import Thread


def receive():

    while True:
        try:
            msg = s.recv(1024).decode("utf-8")
            msg_list.insert(tkinter.END, msg)
        except:
            pass
            break


def send():

    msg = my_msg.get()
    my_msg.set("")
    s.send(bytes(msg, 'utf-8'))

    if msg == '#Quit':
        s.close()
        window.quit()


def on_closing():
    my_msg.set("#Quit")


window = Tk()
window.title("Chat Room")
window.configure(bg='orange')
messages_frame = Frame(window, height=550, width=300, bg='orange')

my_msg = StringVar()
my_msg.set("")

scroll_bar = Scrollbar(messages_frame)
msg_list = Listbox(
    messages_frame, height=27, width=45, bg='white', yscrollcommand=scroll_bar.set
)

scroll_bar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
messages_frame.pack()

btn_lbl = Label(window, text="Enter Your Message", fg='white', bg='blue')
btn_lbl.pack()
entry = Entry(window, textvariable=my_msg, fg='red', width=20)
entry.pack()
send_btn = Button(window, bg='green', fg='white',
                  font='Aerial', text='Send', command=send)
send_btn.pack()
quit_btn = Button(window, bg='red', text='Quit', fg='white',
                  font='Aerial', command=on_closing)
quit_btn.pack()
window.protocol("WN_DELETE_WINDOW", on_closing)

host = '127.0.0.1'
port = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

receive_thread = Thread(target=receive)
receive_thread.start()

mainloop()
