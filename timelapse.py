import sys
from Tkinter import *
from tkFileDialog import askopenfilename
from moviepy.editor import *


def clipSelection():
    clip = VideoFileClip(path)

#creates the file selection gui
def fileSelector():
    Tk().withdraw()
    return askopenfilename()

#creates the cancel button
def quit(root):
    root.quit()

def export(clip):
    time = float(entry_length.get())
    speed = clip.duration/time
    clip_final = clip.fx(vfx.speedx, speed)
    clip_final.write_videofile(entry_export.get())

#select video file
path = fileSelector()
clip = VideoFileClip(path)

#creating tkinter window
root = Tk()
root.title('Hyperlapse Creator')
root.geometry("400x500")

#creates current working labels
current_working_label = Label(root, text = "You are currently working on file: ").grid(row = 0)
working_directory_label = Label(root, text = str(path)).grid(row = 2)
audio_preference = Label(root, text = "Select your audio preference").grid(row = 5)

#creates radio buttons to select audio preference
radioVar = IntVar()
radioVar.set(1)
no_audio = Radiobutton(root, text="No Audio",variable= radioVar, value = 1, command = root.quit()).grid(row = 6)
import_audio = Radiobutton(root, text = "Import Audio", variable = radioVar, value = 2, command = root.quit()).grid(row = 7)
random_audio = Radiobutton(root, text = "Random Audio (from soundcloud)", variable = radioVar, value = 3, command = root.quit()).grid(row = 8)

#creating video length label
video_length = Label(root, text = "\nYour clip is " + str(clip.duration) + " Seconds Long\n").grid(row = 10)

#user entry
desire_length_label = Label(root, text = "Desired Length:").grid(row = 11, column = 0)
entry_length = Entry(root, bd = 5, width = 5)
entry_length.grid(row = 12, column = 0)
seconds_label = Label(root, text = "Seconds\n").grid(row = 13, column = 0)

#export name
file_export_name = Label(root, text = "\nExported File Name:   ").grid(row = 16, column = 0)
entry_export = Entry(root, bd = 5, width = 20)
entry_export.grid(row = 17, column = 0)

export_button = Button(root, text = "Export", command = lambda clip = clip:export(clip)).grid(row = 18)

#cancel button works with sys.exit() to return to command line
cancel_button = Button(root, text = "cancel", command= lambda root = root:quit(root)).grid(row = 19)


#end of tkinter
root.mainloop()

#exits back to command line
sys.exit()

'''
clip = VideoFileClip(path)
length = clip.duration
print 'The video length is currently', length, 'seconds'
desired_time = input('How long would you like the clip to be (in seconds): ')
speed = length/desired_time
print 'Your clip will be sped up', speed, 'times'
clip = clip.fx(vfx.speedx, speed)

#setting the title of the hyperlapse
title = path.split('/')[-1]
title = title.split('.')[0]
title = title + "-lapse.mp4"

clip.write_videofile(title, "-lapse.mp4")
'''
