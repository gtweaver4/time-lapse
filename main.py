import timelapse
import combining_files
import sys
import os
import subprocess
from Tkinter import *
from moviepy.editor import *
from tkFileDialog import askopenfilename

path = ""
audio_path = ""
#this brings the desired tk frame to the front
def raise_frame(frame):
	frame.tkraise()

#creates the cancel button's command
def quit(root):
    root.quit()

#creates the file selection gui
def fileSelector():
    Tk().withdraw()
    return askopenfilename()

#button command from the main menu changes to timelapse view
def start_timelapse():
	global path
	path = fileSelector()
	video_length_text.set("\nYour clip is " + str(VideoFileClip(path).duration) + " Seconds Long\n")
	raise_frame(tl)


#saves path for audio file
def get_audio_path():
    global audio_path 
    audio_path = fileSelector()

#takes in three parameters a path variable linking to the video clip
#the desired length upon completing the timelapse
#and the new file name that will be created
def export(path, length, new_file_name):

    clip = VideoFileClip(path, new_file_name)
    time = float(length)
    speed = clip.duration/time
    #if audio, layer the clips
    if(len(audio_path) > 0):
        clip = clip.fx(vfx.speedx, clip.duration/time)
        #shorten audio in command line
        cmd = 'ffmpeg -ss 0 -t ' + length + ' -i ' + audio_path + ' shortenedAudio.mp3'
        subprocess.call(cmd, shell = True)
        audio = AudioFileClip('shortenedAudio.mp3')
        clip = clip.set_audio(audio)
        clip.write_videofile(new_file_name)
        os.remove('shortenedAudio.mp3')
    #if no audio just combine clipse like normal
    else:
        clip = clip.fx(vfx.speedx, speed)
        clip.write_videofile(new_file_name)

    sys.exit() 

#creates main window
root = Tk()
root.title('Video Editor')
root.geometry('400x500')


#initializes frames that the tk window can swap between
home = Frame(root)
tl = Frame(root)
cf = Frame(root)
cal = Frame(root)

for frame in (home,tl,cf,cal):
	frame.grid(row=0, column=0, sticky='news')

###########
###########
## HOME
###########
###########

title_label = Label(home, text = "Quick Edit",font = ("Helvetica", 25), justify = CENTER).grid(row = 0)


combining_label = Label(home, text = "Combine Video Clips", font = ("Helvetica", 16)).grid(row = 1)
combining_lutton = Button(home, text = "Combine", command= lambda:combining_files.combiningFiles(False)).grid(row = 2)

time_label = Label(home, text = "Create a Timelapse", font = ("Helvetica", 16)).grid(row = 3)
timeButton = Button(home, text = "Timelapse", command = lambda:start_timelapse()).grid(row = 4)

#Combine And Lapse
cal_label = Label(home, text = "Combine then Timelapse", font = ("Helvetica", 16)).grid(row = 5)
cal_lutton = Button(home, text = "Combine & Lapse", command = lambda:combining_files.combiningFiles(True)).grid(row = 6)
cancel_button = Button(home, text = "cancel", command= lambda:quit(root)).grid(row = 7)


############
############
## TIMELAPSE
############
############

#creates current working labels
current_working_label = Label(tl, text = "You are currently working on file: ").grid(row = 0)
working_directory_label = Label(tl, text = str(path)).grid(row = 2)
audio_preference = Label(tl, text = "Select your audio preference").grid(row = 5)

#creates an import button if user wished to import their audio
import_audio_button = Button(tl, text = "Import Audio", command = lambda:get_audio_path()).grid(row = 6)
#creating video length label
video_length_text = StringVar()
video_length = Label(tl, textvariable = video_length_text)
video_length.grid(row = 10)
#user entry
desire_length_label = Label(tl, text = "Desired Length:").grid(row = 11, column = 0)
entry_length = Entry(tl, bd = 5, width = 5)
entry_length.insert(0, "5")
entry_length.grid(row = 12, column = 0)
seconds_label = Label(tl, text = "Seconds\n").grid(row = 13, column = 0)
#export name
file_export_name = Label(tl, text = "\nExported File Name:   ").grid(row = 16, column = 0)
entry_export = Entry(tl, bd = 5, width = 20)
entry_export.insert(0, "timelapse.mp4")
entry_export.grid(row = 17, column = 0)
export_button = Button(tl, text = "Export", command = lambda:export(path,entry_length.get() ,entry_export.get())).grid(row = 18)
#cancel button works with sys.exit() to return to command line
cancel_button = Button(tl, text = "cancel", command= lambda:quit(root)).grid(row = 19)



#sets starting frame as home
raise_frame(home)

#end of tkinter
root.mainloop()