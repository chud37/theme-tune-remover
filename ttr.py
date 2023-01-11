import argparse

import librosa
import time
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# import moviepy.editor as mp
from moviepy.editor import AudioFileClip, CompositeAudioClip
import os
from os import path
import sys

from pathlib import Path


from multiprocessing import Process, Manager
from dotenv import dotenv_values


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
    
    return offset


def getFileList(walk_directory):
    foundFiles = []
    for root, subdirs, files in os.walk(walk_directory):
        for filename in files:
            if ('.mp4' in str(filename) or '.avi' in str(filename) or '.mkv' in str(filename) or '.mov' in str(filename)):
                file_path = os.path.join(root, filename)
                foundFiles.append(Path(file_path))
    return foundFiles

def removeThemeTune(file, outputDirectory, themeFile, themeFileDuration):

    print('\n\n------------------\n', os.path.splitext(Path(file).stem)[0], '\n------------------')
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

def createDirectory(directory):
    if not os.path.exists(directory):
        try:
            os.mkdir(directory)
            print ('Successfully created outputDirectory: ', directory)
            return True
        except:
            raise SystemExit("[ Unable to create directory: ",directory," program fail. ]")
            return False

def pathExists(directory):
        if not path.exists(os.path.abspath(directory)):
            return False
        return True
def getEnvironmentVar(var, environmentItems) -> str:
        for key, value in environmentItems.items():
            if key == var:
                return value
        return ''

def loadEnvironmentalData():
    thisFilePath = os.path.dirname(os.path.realpath(__file__))
    environmentFileLocal = os.path.join(thisFilePath,'.env.local')
    environmentFileDist = os.path.join(thisFilePath,'.env.dist')
    if pathExists(environmentFileLocal):
        return dotenv_values(environmentFileLocal)
    else:
        source = Path(environmentFileDist)
        destination = Path(environmentFileLocal)
        destination.write_bytes(source.read_bytes())
        return dotenv_values(environmentFileLocal)
    
    

def main():

    print ('\n\n----------------------------------------------------------------')
    print ('Theme Tune Remover')
    print ('Supply a directory and place a file with theme tune to cutout in the root of that directory.  Name it theme.wav\n')
    print ('You may need to update your moviepy file as per this pull request: https://github.com/Zulko/moviepy/pull/1757/files')
    print ('Update the readers.py file and this will prevent any Index out of bounds errors.\n')
    print ('Preparing to cut the theme tune out of all video files and save as audio files...')
    print ('----------------------------------------------------------------\n\n')

    # Get environment data, namely the video path that we'll scan for video files in.
    environmentData = loadEnvironmentalData()
    videoDirectory = getEnvironmentVar('VIDEO_PATH', environmentData)
    themeFile = Path(os.path.join(videoDirectory, 'theme.wav'))

    if not os.path.exists(themeFile):
        print('Theme file not found in ', themeFile)
        raise SystemExit('Unable to find theme file..  Please create wav file named theme.wav in the target directory.')

    themeFileDuration = librosa.get_duration(filename=themeFile)
    files = getFileList(videoDirectory)
    
    outputDirectory = Path(os.path.join(videoDirectory,'themeTuneRemoved'))
    createDirectory(outputDirectory)
    
    with Manager() as manager:
        managerList = manager.list()
        processList = []
    
        for file in files:
            process = Process(target=removeThemeTune, args=(file, outputDirectory, themeFile, themeFileDuration))
            process.start()
            process.join()
            process.terminate() 
            
        print(managerList)
    

if __name__ == '__main__':
    main()