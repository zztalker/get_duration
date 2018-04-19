import os
import sys
from ffprobe3 import FFProbe

total_duration = 0.0
cnt = 0
verbose = '--v' in sys.argv
only_errors = '--errors' in sys.argv

if len(sys.argv)==1:
    print(
"""Usage: python get_duration path [--v] 

    --v verbose mode (for debugging purpose)
    --errors print file name when an error occurred while extracting duration time (corrupted video?)
    
    Recursively pathing through the directory and calculate total duration of mp4,mov,avi files.
    Depends on ffprobe, must be accesible in current dir.
    """)
    exit()

def checkDir(dirname):
    global total_duration
    global cnt
    global verbose
    global only_errors
    for f in os.scandir(dirname):
        if f.is_dir():
            checkDir(f.path)
        else:
            if f.name[-3:] in ['mp4','mov','avi']:
                cnt += 1
                try:
                    metadata=FFProbe(f.path)
                except:
                    if verbose or only_errors:
                        print('Error in file',f.path)
                    continue
                duration_vs = 0.0
                for stream in metadata.streams:
                    if stream.is_video():
                        duration_vs+=stream.duration_seconds()
                if verbose:
                    print(f.name, "duration by video streams:", duration_vs)
                total_duration += duration_vs

checkDir(sys.argv[1])
print("Videos count:", cnt)
m,s = divmod(total_duration, 60)
h,m = divmod(m, 60)
print(f"Total duration: {h:.0f}:{m:02.0f}:{s:02.3f}")