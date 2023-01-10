import argparse

import librosa
import time
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# import moviepy.editor as mp
from moviepy.editor import AudioFileClip, CompositeAudioClip
import os
import sys

from pathlib import Path
import gc

# Theme Tune Remover
# -----------------------------------------------
# To run:
# conda activate themeTuneRemover
# python ttr.py


# https://github.com/Zulko/moviepy/pull/1757/files



def findOffset(within_file, find_file, window):
    y_within, sr_within = librosa.load(within_file, sr=None)
    y_find, _ = librosa.load(find_file, sr=sr_within)

    c = signal.correlate(y_within, y_find[:sr_within*window], mode='valid', method='fft')
    peak = np.argmax(c)
    offset = round(peak / sr_within, 2)

    fig, ax = plt.subplots()
    ax.plot(c)
    
    del y_within, sr_within, y_find, ax, fig, peak, c
    gc.collect()
    
    return offset


def getFileList(walk_directory):
    foundFiles = []
    for root, subdirs, files in os.walk(walk_directory):
        for filename in files:
            if ('.mp4' in str(filename) or '.avi' in str(filename) or '.mkv' in str(filename) or '.mov' in str(filename)):
                file_path = os.path.join(root, filename)
                foundFiles.append(Path(file_path))
    return foundFiles

def convertToAudioFiles(files, directory):
    global themeFile

    themeFileDuration = librosa.get_duration(filename=themeFile)

    outputDirectory = Path(os.path.join(directory,'output'))
    createDirectory(outputDirectory)

    for index, file in enumerate(files):

        print('\n\n------------------\n', os.path.splitext(Path(file).stem)[0], '\n------------------')

#         audioFileName = os.path.splitext(file.replace(directory, outputDirectory))[0]+".wav"
        audioFileName = str(Path(os.path.join(outputDirectory, os.path.splitext(Path(file).stem)[0]+'.wav')))
        cutoutAudioFileName = str(Path(os.path.join(outputDirectory, os.path.splitext(Path(file).stem)[0]+'_cutout.wav')))

        audioclip = AudioFileClip(str(file))
        audioclip.write_audiofile(audioFileName)
        offset = findOffset(audioFileName, themeFile, 90)

        offsetTime = time.strftime("%H:%M:%S", time.gmtime(offset))
        offsetTimeAndTheme = time.strftime("%H:%M:%S", time.gmtime(offset + themeFileDuration))

        print('\nFound offset:', offset, '- Writing audio file again...')
        print('Cutting audio from', str(offsetTime), 'to', str(offsetTimeAndTheme))

        cutout = audioclip.cutout(offsetTime, offsetTimeAndTheme)
        cutout.write_audiofile(audioFileName)
        audioclip.close()
        cutout.close()
        
        del audioclip
        del cutout
        
        gc.collect()

        


def createDirectory(directory):
    if not os.path.exists(directory):
        try:
            os.mkdir(directory)
            return True
        except:
            raise SystemExit("[ Unable to create directory: ",directory," program fail. ]")
            return False

def main():
    global themeFile

    print ('\n\n----------------------------------------------------------------')
    print ('Theme Tune Remover')
    print ('Supply a directory and place a file with theme tune to cutout in the root of that directory.  Name it theme.wav\n')
    print ('You may need to update your moviepy file as per this pull request: https://github.com/Zulko/moviepy/pull/1757/files')
    print ('Update the readers.py file and this will prevent any Index out of bounds errors.\n')
    print ('Preparing to cut the theme tune out of all video files and save as audio files...')
    print ('----------------------------------------------------------------\n\n')

    # directory = '/Users/chud37/Desktop/Friends'
    directory = 'M:/tv/Friends/process'
    themeFile = Path(os.path.join(directory, 'theme.wav'))

    if not os.path.exists(themeFile):
        print('Theme file not found in ', themeFile)
        raise SystemExit('Unable to find theme file..  Please create wav file named theme.wav in the target directory.')

    files = getFileList(directory)
    convertToAudioFiles(files, directory)

if __name__ == '__main__':
    main()