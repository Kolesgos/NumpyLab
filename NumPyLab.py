# -*- coding: utf-8 -*-

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os

def GetImg(fileName):
    image = Image.open(fileName)
    arr = np.array(image.convert("L"))
    return arr

def midFilt(data, width):
    for i in range(len(data)):
        data[i] = np.mean(data[max(0, i - width):i+1])
    return data

def nextStep(data, A):
    return data - 0.5*np.dot(A, data)
    
def animate(i):
    x = list(range(len(animation[i])))
    y = animation[i]
    line.set_data(x, y)
    return line,

def init():
    line.set_data([], [])
    return line,   
    
#Для работы необходима папка lunar_images в той же дирректории, что и программа и 
#папка CONV в папке lunar_images (туда сохраняются обработанные изображения)
def Ep1():
    dirr = "lunar_images"
    files = os.listdir(dirr)
    for file in files:
        if (file[-4:] == '.jpg'):
            pic = GetImg(os.path.join(dirr, file))
            min_ = np.amin(pic)
            max_ = np.amax(pic)
            LUT = np.zeros(256, dtype = np.uint8)
            LUT[min_ : max_ + 1]=np.linspace(start = 0, stop = 255, num = max_ - min_ + 1, endpoint = True, dtype = np.uint8)
            Image.fromarray(LUT[pic]).save(os.path.join(dirr, 'CONV', 'CONV' + file))
      
#Для работы необходима папка signals в той же дирректории, что и программа      
def Ep2():
    dirr = "signals"
    files = os.listdir(dirr)
    for file in files:
        if (file[-4:] == '.dat'):   
            data = np.genfromtxt(os.path.join(dirr, file))
            fig, axs = plt.subplots(2, 1)
            axs[0].plot(list(range(len(data))), data)
            axs[1].plot(list(range(len(data))), midFilt(data, 10))
            fig.savefig(os.path.join(dirr, file[:-3] + 'pdf'))    
            
#Для работы необходима папка func в той же дирректории, что и программа   
#При просмотре в генерируемом окне есть какие-то проблемы, но в сохраняемом файле все Ок.

dirr = "func"
files = os.listdir(dirr)
frames = 1000
for file in files:
    if (file[-4:] == '.dat'): 
        data = np.genfromtxt(os.path.join(dirr, file))
        A = np.identity(len(data), dtype=float) - np.eye(len(data), k=-1, dtype=float)
        A[0][-1] = -1
        animation = []
        for i in range(frames):
            animation.append(data)
            data = nextStep(data, A)
        fig = plt.figure()
        ax = plt.axes(xlim=(0, 50), ylim=(0, 10))
        line, = ax.plot([], [], lw=3)        
        anim = FuncAnimation(fig, animate, init_func=init, frames=frames, interval=80, blit=True)   
        anim.save(os.path.join(dirr, file[:-3] + 'gif'), writer='imagemagick')
