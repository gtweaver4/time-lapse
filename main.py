import timelapse
import combining_files
import sys
from Tkinter import *

#creates main window
root = Tk()
root.title('Video Editor')
root.geometry('400x500')

titleLabel = Label(root, text = "Quick Edit",font = ("Helvetica", 25), justify = CENTER).grid(row = 0)


combiningLabel = Label(root, text = "Combine Video Clips", font = ("Helvetica", 16)).grid(row = 1)
combiningButton = Button(root, text = "Combine", command= lambda root = root:combining_files.combiningFiles(False)).grid(row = 2)

timeLabel = Label(root, text = "Create a Timelapse", font = ("Helvetica", 16)).grid(row = 3)
timeButton = Button(root, text = "Timelapse", command = lambda root = root:timelapse.runTimelapse()).grid(row = 4)

#Combine And Lapse
calLabel = Label(root, text = "Combine then Timelapse", font = ("Helvetica", 16)).grid(row = 5)
calButton = Button(root, text = "Combine & Lapse", command = lambda root = root:combining_files.combiningFiles(True)).grid(row = 6)
cancel_button = Button(root, text = "cancel", command= lambda root = root:quit(root)).grid(row = 7)

#end of tkinter
root.mainloop()


#'last resort' system exit
sys.exit()
