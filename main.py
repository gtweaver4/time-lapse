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
	#reset variables if returning home
	if(frame == home):
		global path, audio_path, clip_list, path_list
		path = ""
		audio_path = ""
		clip_list = []
		path_list = []
		tv_audio.set("Import Audio: (optional)")
		tv_dir.set("")

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
	tv_dir.set(str(path) + "\n\n")
	try:
	    video_length_text.set("\nYour clip is " + str(VideoFileClip(path).duration) + " Seconds Long\n\n")
	except:
		print("error processing clip: " + str(path) + "\nPlease use standard video formats (mp4,flv,mov)")
	raise_frame(tl)


#
# TIMELAPSE FUNCTIONS
#

#saves path for audio file
def get_audio_path():
    global audio_path 
    audio_path = fileSelector()
    tv_audio.set("Audio: " + audio_path)

#takes in three parameters a path variable linking to the video clip
#the desired length upon completing the timelapse
#and the new file name that will be created
def export(path, length, new_file_name):
	#checks if clips is valid file type
    try:
        clip = VideoFileClip(path, new_file_name)
    except:
        print('error processing clip: ' + str(path) + "\nPlease use standard video formats (mp4,flv,mov)")
        return

    #makes sure time is valid (not letters or 0)
    try:
    	time = float(length)
    	speed = clip.duration/time
    except:
    	print('invalid time input')
    	return

    #if audio, layer the clips
    if(len(audio_path) > 0):
        clip = clip.fx(vfx.speedx, clip.duration/time)

        #shorten audio in command line & ensure ffmpeg is installed
        try:
        	cmd = 'ffmpeg -ss 0 -t ' + length + ' -i ' + audio_path + ' shortenedAudio.mp3'
        	subprocess.call(cmd, shell = True)
        	audio = AudioFileClip('shortenedAudio.mp3')
        	clip = clip.set_audio(audio)
        except:
        	print('error processing audio with ffmpeg please ensure \'ffmpeg\' is installed')
        
        clip.write_videofile(new_file_name)
        os.remove('shortenedAudio.mp3')
    #if no audio just combine clipse like normal
    else:
        clip = clip.fx(vfx.speedx, speed)
        clip.write_videofile(new_file_name)

    quit(root)


#this takes the clip itself as a parameter to use with combine and lapse
#the length and exported file name is also used
def export_with_clip(clip, length, new_file_name):
    
    #makes sure time is valid (not letters or 0)
    try:
    	time = float(length)
    	speed = clip.duration/time
    except:
    	print('invalid time input')
    	return

    #if audio, layer the clips
    if(len(audio_path) > 0):
        clip = clip.fx(vfx.speedx, clip.duration/time)

        #shorten audio in command line & ensure ffmpeg is installed
        try:
        	cmd = 'ffmpeg -ss 0 -t ' + length + ' -i ' + audio_path + ' shortenedAudio.mp3'
        	subprocess.call(cmd, shell = True)
        	audio = AudioFileClip('shortenedAudio.mp3')
        	clip = clip.set_audio(audio)
        except:
        	print('error processing audio with ffmpeg please ensure \'ffmpeg\' is installed')
        
        clip.write_videofile(new_file_name)
        os.remove('shortenedAudio.mp3')
    #if no audio just combine clipse like normal
    else:
        clip = clip.fx(vfx.speedx, speed)
        clip.write_videofile(new_file_name)

    quit(root)



#
# COMBINING FUNCTIONS
#

#adds the path to list so it can be accessed later
def import_video(gridVal, frame):
    path_list.append(fileSelector())
    #-1 will get the most recent added to path_list
    clip_list.append(VideoFileClip(path_list[-1]))
    i = 1
    for x in path_list:
    	Label(frame, text = str(i) + ": Clip: " + path_list[-1] + " added").grid(row = gridVal)
    	gridVal +=1
    	i +=1
    

def combined_export(file_name):
    try:
    	final_clip = concatenate_videoclips(clip_list)
    	final_clip.write_videofile(file_name)
    except:
    	print('Error when processing video files \nPlease use standard video formats (mp4,flv,mov)')
    
    quit(root)


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
root.geometry('500x500')

#this is what sets the row and col to center allignment
root.rowconfigure(0,weight = 1)
root.columnconfigure(0,weight = 1)

#initializes frames that the tk window can swap between
home = Frame(root)
tl = Frame(root)
cf = Frame(root)
cal = Frame(root)


for frame in (home,tl,cf,cal):
	frame.grid(row=0, column=0, sticky='news')
	frame.rowconfigure(0, weight = 1)
	frame.columnconfigure(0, weight = 1)

###########
###########
## HOME
###########
###########

Label(home, text = "Quick Edit",font = ("Helvetica", 25), justify = CENTER).grid(row = 0)

Label(home, text = "Combine Video Clips", font = ("Helvetica", 16)).grid(row = 1)
Button(home, text = "Combine", command= lambda:raise_frame(cf)).grid(row = 2)

Label(home, text = "Create a Timelapse", font = ("Helvetica", 16)).grid(row = 3)
Button(home, text = "Timelapse", command = lambda:start_timelapse()).grid(row = 4)

#Combine And Lapse
Label(home, text = "Combine then Timelapse", font = ("Helvetica", 16)).grid(row = 5)
Button(home, text = "Combine & Lapse", command = lambda:raise_frame(cal)).grid(row = 6)
Button(home, text = "cancel", command= lambda:quit(root)).grid(row = 7)
Label(home, text = "\n\n\n\n").grid(row = 999)

##########################
##########################
## TIMELAPSE 	##########
##########################
##########################

#creates current working labels
Label(tl, text = "TimeLapse").grid(row = 0)
Label(tl, text = "You are currently working on file: ").grid(row = 1)
tv_dir = StringVar()
tl_dir_label = Label(tl, textvariable = tv_dir)
tl_dir_label.grid(row = 2)

tv_audio = StringVar()
tv_audio.set("Import Audio: (optional)")
audio_label = Label(tl, textvariable = tv_audio)
audio_label.grid(row = 5)

#creates an import button if user wished to import their audio
Button(tl, text = "Import Audio", command = lambda:get_audio_path()).grid(row = 6)
#creating video length label
video_length_text = StringVar()
video_length = Label(tl, textvariable = video_length_text)
video_length.grid(row = 10)

#user entry
tl_entry_frame = Frame(tl)

Label(tl_entry_frame, text = "Desired Length:").pack(side = LEFT)
entry_length = Entry(tl_entry_frame, bd = 5, width = 5)
entry_length.insert(0, "5")
entry_length.pack(side = LEFT)
Label(tl_entry_frame, text = "Seconds").pack(side = LEFT)

tl_entry_frame.grid(row = 11)

#export name
Label(tl, text = "\nExported File Name:   ").grid(row = 16, column = 0)
entry_export = Entry(tl, bd = 5, width = 20)
entry_export.insert(0, "timelapse.mp4")
entry_export.grid(row = 17, column = 0)

tl_button_frame = Frame(tl)

Button(tl_button_frame, text = "Export", command = lambda:export(path,entry_length.get() ,entry_export.get())).pack(side = LEFT)
Button(tl_button_frame, text = "Back" , command = lambda: raise_frame(home)).pack(side = LEFT)
Button(tl_button_frame, text = "cancel", command= lambda:quit(root)).pack(side = LEFT)

tl_button_frame.grid(row = 18)
Label(tl, text = "\n\n\n\n").grid(row = 999)
##########################
##########################
## COMBINING 	##########
##########################
##########################



Label(cf, text = "Combining Files").grid(row = 0)
Label(cf, text = "Select the clips you wish to import").grid(row = 1)
Button(cf, text = "Import Video", command = lambda:import_video(7,cf)).grid(row = 3)
Label(cf, text = "\nExported File Name:").grid(row = 4)
export_name = Entry(cf, bd = 5, width = 20)
export_name.insert(0 , "combined.mp4")
export_name.grid(row = 5)

cf_button_frame = Frame(cf)
Button(cf_button_frame, text = "Export", command = lambda:combined_export(export_name.get())).pack(side = LEFT)
Button(cf_button_frame, text = "Back" , command = lambda: raise_frame(home)).pack(side = LEFT)
Button(cf_button_frame, text = "Cancel", command = lambda:quit(root)).pack(side = LEFT)
cf_button_frame.grid(row = 6)
Label(cf, text = "\n\n\n\n").grid(row = 999)
##########################
##########################
## COMBINE AND LAPSE 	##
##########################
##########################

Label(cal, text = "Combining Files\n").grid(row = 0)
Label(cal, text = "Select the clips you wish to import:").grid(row = 1)
import_button = Button(cal, text = "Import Video", command = lambda:import_video(15,cal)).grid(row = 2)


tv_audio.set("\nImport Audio: (optional)")
cal_audio_label = Label(cal, textvariable = tv_audio)
cal_audio_label.grid(row = 3)

#creates an import button if user wished to import their audio
Button(cal, text = "Import Audio", command = lambda:get_audio_path()).grid(row = 4)





Label(cal, text = "\nDesired Length:").grid(row = 5)
cal_length = Entry(cal, bd = 5, width = 5)
cal_length.insert(0, "5")
cal_length.grid(row = 6)
Label(cal, text = "\nExported File Name: ").grid(row = 7)
cal_name = Entry(cal, bd = 5, width = 20)
cal_name.insert(0 , "combinedAndLapsed.mp4")
cal_name.grid(row = 8)

cal_button_frame = Frame(cal)
Button(cal_button_frame, text = "Export", command = lambda:start_cal(cal_length.get(),cal_name.get())).pack(side = LEFT)
Button(cal_button_frame, text = "Back" , command = lambda: raise_frame(home)).pack(side = LEFT)
Button(cal_button_frame, text = "Cancel", command = lambda:quit(root)).pack(side = LEFT)
cal_button_frame.grid(row = 9)
Label(cal, text = "\n\n\n\n").grid(row = 999)

#sets starting frame as home
raise_frame(home)

#end of tkinter
root.mainloop()
