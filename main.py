# https://www.youtube.com/watch?v=iZUcX4kYrSM

from tkinter import Tk, PhotoImage
from Frontend import FrontEnd

if __name__ == "__main__":        
    mainWindow = Tk()
    mainWindow.title("Photoshop")
    mainWindow.iconphoto(False, PhotoImage(file='D:\\VS_CODE\\AI\\DigitalImageProcessing\\Final_Project\\Image-Processing-21\\icon.png'))
    # mainWindow.geometry("1200x600")
    FrontEnd(mainWindow)
    mainWindow.mainloop()