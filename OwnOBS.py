from PIL import ImageGrab, ImageTk
import numpy as np
import cv2
import time
import keyboard
from tkinter import *
from mss import mss
import pygifsicle
import threading

def SwitchEnd():
    print('Done')
    global IsEnd
    IsEnd = True

def newproc():
    x = threading.Thread(target=ScreenRecorder)
    x.start()

def ScreenRecorder():
    print('STARTED')
    my_gui.btnStart.config(state='disabled')
    my_gui.btnStop.config(state='normal')
    global IsEnd
    IsEnd = False
    ScreenList = []
    #ScreenList = np.array(ImageGrab.grab())
    #print(ScreenList.shape)
    #np.append(ScreenList, ImageGrab.grab())
    #print(ScreenList.shape)
    #ScreenList = []

    start = time.time()
    process = Label(my_gui.frame,text="Recording")
    process.pack()
    while True:
        mss().compression_level = 2
        img = ImageGrab.grab()
        ScreenList.append(img)
        time.sleep(0.15)

        if IsEnd:
            end = time.time()
            process.config(text="processing")
            my_gui.btnStop.config(state='disabled')
            break

    deltatime = end - start
    print(len(ScreenList))
    ScreenList[0].save('out.gif', loop = True, save_all = True, append_images=ScreenList[1:], optimize = True,
                       duration = (deltatime * 1000 / len(ScreenList)))
    pygifsicle.optimize("out.gif")
    process.config(text='Completed!')
    process.after(5000,process.destroy)
    my_gui.btnStart.config(state='normal')


class GUI:
    def __init__(self,master):
        self.master = master
        master['bg'] = 'grey'
        master.title('Giffer')
        master.geometry('600x550')

        self.frame = Frame(master, bg = 'gray')
        self.frame.place(relwidth=1, relheight=1)

        title = Label(self.frame, text="GIF Capture",bg='gray', font=("Arial",35))
        title.pack()

        self.btnStart = Button(self.frame,state='normal', text='Start',fg='white',width=20, bg='black',font=("Arial",10),
                            command=newproc)
        self.btnStart.place(relx=0.1,rely=0.8)

        self.btnStop = Button(self.frame,state='disabled', text='Stop',fg='white',width=20, bg='black',
                              font=("Arial",10), command=SwitchEnd)
        self.btnStop.place(relx=0.6,rely=0.8)


if (__name__ == '__main__'):
    IsEnd = False
    root = Tk()
    my_gui = GUI(root)
    root.mainloop()
