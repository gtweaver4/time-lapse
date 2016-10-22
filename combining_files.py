import timelapse
from moviepy.editor import *
from Tkinter import *
import sys

clip_array = []
path_array = []
i = 0

def combiningFiles(cal):
    root = Tk()
    root.title("Combining Clips")
    root.geometry("400x500")

    title_label = Label(root, text = "Combining Files").grid(row = 0)
    selector_label = Label(root, text = "Select the clips you wish to import").grid(row = 1)
    import_button = Button(root, text = "Import Video", command = lambda root = root:importVideo()).grid(row = 3)
    export_name = Entry(root, bd = 5, width = 20)
    export_name.insert(0 , "combined.mp4")
    export_name.grid(row = 4)

    finished_button = Button(root, text = "finished", command = lambda root = root:exportVideo(cal)).grid(row = 5)
    cancel_button = Button(root, text = "Cancel", command = lambda root = root:sys.exit()).grid(row = 6)

    #end tkinter
    root.mainloop()
    sys.exit()


def importVideo():
    global i
    path_array.append(timelapse.fileSelector())
    clip_array.append(VideoFileClip(path_array[i]))
    print("File: " + path_array[i] + " added")
    i += 1

#is combined and lapsed
def exportVideo(isCAL):
    global export_name
    final_clip = concatenate_videoclips(clip_array)

    if(isCAL):
        timelapse.runTimeLapseWithVideoClip(final_clip)
    else:
        final_clip.write_videofile("combined_testing.mp4")
        sys.exit()
