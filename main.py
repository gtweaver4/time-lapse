import combining_files
import sys
import os
import subprocess
from Tkinter import *
from moviepy.editor import *
from tkFileDialog import askopenfilename

path = ""
audio_path = ""
clip_list = []
path_list = []


#
# MAIN WINDOW FUNCTIONS
#

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


#
# TIMELAPSE FUNCTIONS
#

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


#this takes the clip itself as a parameter to use with combine and lapse
#the length and exported file name is also used
def export_with_clip(clip, length, new_file_name):
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



#
# COMBINING FUNCTIONS
#

#adds the path to list so it can be accessed later
def import_video(gridVal):
    path_list.append(fileSelector())
    #-1 will get the most recent added to path_list
    clip_list.append(VideoFileClip(path_list[-1]))
    gridVal = 7
    i = 1
    for x in path_list:
    	Label(cf, text = str(i) + ": Clip: " + path_list[-1] + " added").grid(row = gridVal)
    	gridVal +=1
    	i +=1
    

def combined_export(file_name):
    final_clip = concatenate_videoclips(clip_list)
    final_clip.write_videofile(file_name)
    raise_frame(home)


#
# COMBINE AND LAPSE FUNCTIONS
#
def start_cal(length, export_name):
	final_clip = concatenate_videoclips(clip_list)
	export_with_clip(final_clip,length,export_name)



#
# TK WINDOWS
#

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
combining_lutton = Button(home, text = "Combine", command= lambda:raise_frame(cf)).grid(row = 2)

time_label = Label(home, text = "Create a Timelapse", font = ("Helvetica", 16)).grid(row = 3)
timeButton = Button(home, text = "Timelapse", command = lambda:start_timelapse()).grid(row = 4)

#Combine And Lapse
cal_label = Label(home, text = "Combine then Timelapse", font = ("Helvetica", 16)).grid(row = 5)
cal_lutton = Button(home, text = "Combine & Lapse", command = lambda:raise_frame(cal)).grid(row = 6)
cancel_button = Button(home, text = "cancel", command= lambda:quit(root)).grid(row = 7)


##########################
##########################
## TIMELAPSE 	##########
##########################
##########################

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


##########################
##########################
## COMBINING 	##########
##########################
##########################



title_label = Label(cf, text = "Combining Files").grid(row = 0)
selector_label = Label(cf, text = "Select the clips you wish to import").grid(row = 1)
import_button = Button(cf, text = "Import Video", command = lambda:import_video(7)).grid(row = 3)
export_name = Entry(cf, bd = 5, width = 20)
export_name.insert(0 , "combined.mp4")
export_name.grid(row = 4)
finished_button = Button(cf, text = "finished", command = lambda:combined_export(export_name.get())).grid(row = 5)
combcancel_button = Button(cf, text = "Cancel", command = lambda:quit(root)).grid(row = 6)


##########################
##########################
## COMBINE AND LAPSE 	##
##########################
##########################

Label(cal, text = "Combining Files").grid(row = 0)
Label(cal, text = "Select the clips you wish to import").grid(row = 1)
import_button = Button(cal, text = "Import Video", command = lambda:import_video(12)).grid(row = 2)
Label(cal, text = "Desired Length:").grid(row = 3)
cal_length = Entry(cal, bd = 5, width = 5)
cal_length.insert(0, "5")
cal_length.grid(row = 6)
Label(cal, text = "Exported File Name: ").grid(row = 7)
cal_name = Entry(cal, bd = 5, width = 20)
cal_name.insert(0 , "combinedAndLapsed.mp4")
cal_name.grid(row = 8)
Button(cal, text = "Export", command = lambda:start_cal(cal_length.get(),cal_name.get())).grid(row = 9)
Button(cal, text = "Cancel", command = lambda:quit(root)).grid(row = 10)



#sets starting frame as home
raise_frame(home)

#end of tkinter
root.mainloop()