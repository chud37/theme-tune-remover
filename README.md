# Theme-Tune-Remover
Given a folder with video files inside & a wav file of the theme tune this script will find & remove the theme tune and save an audio file of the results.

# Why?
I listen to different tv shows when I go to sleep and I'm sick of hearing the same theme song over and over again.  Finally I have developed this tool to remove 
the theme tune and convert to .wav file.  Its much more relaxing to listen to.


# Installation
* Download [Anaconda](https://www.anaconda.com/)
* Run the Anaconda Command Prompt, and inside that the following commands:
```
conda create -n themeTuneRemover python=3.6
conda activate themeTuneRemover
pip install -r requirements.txt
```

# Usage
* Simply run conda activate from with the anaconda prompt: `conda activate themeThuneRemover` 
* Create (or update) the `.env.local` file and write the specified directory inside it. (Don't worry about subdirectories, themeTuneRemover will find all files ending in `.mp4`, `.mov`, `.avi`, `.mkv` and work through the list.)
* Create a .wav file of the theme tune *only*.  You'll need an audio editor for this, like [Goldwave](https://www.goldwave.com/release.php) or [Audicity](https://www.audacityteam.org/download/) - and place it in the directory that you supplied in the `.env.local` file.  
* Navigate to the directory where you git cloned this repository, and run `python ttr.py`.  

# Todo
* Instead of creating `.wav` files I want it to create `.mp3` and have the attributes read from the `.env.local` file, however when I tested this the sound files doubled themselves up for some reason, so further testing is requried.  At the moment I'm just batch processing the `.wav`'s in Goldwave to convert them to `.mp3`.


# Note:
If you get an IndexError: Index out of bounds then you'll need to update the `readers.py` file in the moviepy env directory.
Insert the code from this pull request into readers.py: https://github.com/Zulko/moviepy/pull/1757/files

