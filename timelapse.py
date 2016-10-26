import sys
from tkinter import *
from tkinter import filedialog
from moviepy.editor import *
import subprocess
import os

#creates the file selection gui
def fileSelector():
    Tk().withdraw()
    return filedialog.askopenfilename()

#saves path for audio file
def get_audio_path():
    global audio_path 
    audio_path = fileSelector()
    
#define audio path so that it can be used
#to determine if get_audio_path has been called
audio_path = ""

#creates the cancel button's command
def quit(root):
    root.quit()

#running timelapse 
def runTimelapseWithPath(path):
    #these functions have to be defined within the function
    #because the otherwise the .get() methods to do work
    def export(path):
        clip = VideoFileClip(path)
        time = float(entry_length.get())
        speed = clip.duration/time
        #if audio, layer the clips
        if(len(audio_path) > 0):
            clip = clip.fx(vfx.speedx, clip.duration/time)
            #shorten audio in command line
            cmd = 'ffmpeg -ss 0 -t ' + entry_length.get() + ' -i ' + audio_path + ' shortenedAudio.mp3'
            subprocess.call(cmd, shell = True)
            audio = AudioFileClip('shortenedAudio.mp3')
            clip = clip.set_audio(audio)
            clip.write_videofile(entry_export.get())
            os.remove('shortenedAudio.mp3')
        #if no audio just combine clipse like normal
        else:
            clip = clip.fx(vfx.speedx, speed)
            clip.write_videofile(entry_export.get())

        sys.exit() 

    #creating tkinter window
    root = Tk()
    root.title('Timelapse Creator')
    root.geometry("400x500")

    #creates current working labels
    current_working_label = Label(root, text = "You are currently working on file: ").grid(row = 0)
    working_directory_label = Label(root, text = str(path)).grid(row = 2)
    audio_preference = Label(root, text = "Select your audio preference").grid(row = 5)

    #creates an import button if user wished to import their audio
    import_audio_button = Button(root, text = "Import Audio", command = lambda root = root:get_audio_path()).grid(row = 6)

    #creating video length label
    video_length = Label(root, text = "\nYour clip is " + str(VideoFileClip(path).duration) + " Seconds Long\n").grid(row = 10)

    #user entry
    desire_length_label = Label(root, text = "Desired Length:").grid(row = 11, column = 0)
    entry_length = Entry(root, bd = 5, width = 5)
    entry_length.insert(0, "5")
    entry_length.grid(row = 12, column = 0)
    seconds_label = Label(root, text = "Seconds\n").grid(row = 13, column = 0)

    #export name
    file_export_name = Label(root, text = "\nExported File Name:   ").grid(row = 16, column = 0)
    entry_export = Entry(root, bd = 5, width = 20)
    entry_export.insert(0, "timelapse.mp4")
    entry_export.grid(row = 17, column = 0)

    export_button = Button(root, text = "Export", command = lambda path = path:export(path)).grid(row = 18)

    #cancel button works with sys.exit() to return to command line
    cancel_button = Button(root, text = "cancel", command= lambda root = root:quit(root)).grid(row = 19)

    #end of tkinter
    root.mainloop()

    #exits back to command line as a 'last resort'
    sys.exit()

#running timelapse with a file selector for the timelapse button
def runTimelapse():
    path = fileSelector()
    runTimelapseWithPath(path)


def runTimeLapseWithVideoClip(VideoClip):
    def exportClip(VideoClip):
        #function in function so .get() method works
        global exportClip
        clip = VideoClip
        time = float(entry_length.get())
        speed = clip.duration/time
        #if audio, layer the clips
        if(len(audio_path) > 0):
            clip = clip.fx(vfx.speedx, clip.duration/time)
            #shorten audio in command line
            cmd = 'ffmpeg -ss 0 -t ' + entry_length.get() + ' -i ' + audio_path + ' shortenedAudio.mp3'
            subprocess.call(cmd, shell = True)
            audio = AudioFileClip('shortenedAudio.mp3')
            clip = clip.set_audio(audio)
            clip.write_videofile(entry_export.get())
            os.remove('shortenedAudio.mp3')
        #if no audio just combine clipse like normal
        else:
            clip = clip.fx(vfx.speedx, speed)
            clip.write_videofile(entry_export.get())

        sys.exit()
    #creating tkinter window
    root = Tk()
    root.title('Timelapse Creator')
    root.geometry("400x500")
    audio_preference = Label(root, text = "Select your audio preference").grid(row = 5)

    #creates an import button if user wished to import their audio
    import_audio_button = Button(root, text = "Import Audio", command = lambda root = root:get_audio_path()).grid(row = 6)
    #creating video length label
    video_length = Label(root, text = "\nYour clip is " + str(VideoClip.duration) + " Seconds Long\n").grid(row = 10)
    #user entry
    desire_length_label = Label(root, text = "Desired Length:").grid(row = 11, column = 0)
    entry_length = Entry(root, bd = 5, width = 5)
    entry_length.insert(0, "5")
    entry_length.grid(row = 12, column = 0)
    seconds_label = Label(root, text = "Seconds\n").grid(row = 13, column = 0)
    #export name
    file_export_name = Label(root, text = "\nExported File Name:   ").grid(row = 16, column = 0)
    entry_export = Entry(root, bd = 5, width = 20)
    entry_export.insert(0, "timelapse.mp4")
    entry_export.grid(row = 17, column = 0)
    export_button = Button(root, text = "Export", command = lambda root = root:exportClip(VideoClip)).grid(row = 18)

    #cancel button works with sys.exit() to return to command line
    cancel_button = Button(root, text = "cancel", command= lambda root = root:quit(root)).grid(row = 19)

    #end of tkinter
    root.mainloop()
