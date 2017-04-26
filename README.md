# time-lapse
Creates a GUI interface to make time-lapse videos and quickly edit videos.
This program uses tkinter to make a lightweight editor window that can easily run
in the background. This makes it easy to turn any length of video into a clip of your desired length.

The simple alogorithm is video_length/desired_length to lengthen
or shorten the clip accordingly. The audio is edited by using ffmpeg in the shell. This
is because there did not appear to be a good library for adding audio to clips. When I asked
on forums, I recieved the answer ffmpeg could be more simple then trying to work with libraries
or working manual on the problem. 

I added functionality of being able to combine clips, timelapse, and both at the same time.
This was added because many recording softwares will break giant recorded files into seperate files
when the scene changes.

This program has only been tested on linux so far. I assume it will not function
properly in windows as it does call the shell to use ffmpeg to handle audio. 
It has been tested mainly using videos of ~60 seconds in length for quick testing,
but I did test with one 3 and 4 hour long video. While it did work, the rendering took
~30 minutes which is to be expected from larger files needing to be edited.
 
There is a similar feature in adobe premiere pro that has inspired
this program.
