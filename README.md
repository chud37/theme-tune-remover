# theme-tune-remover
Given a folder with video files inside & a wav file of the theme tune this script will find & remove the theme tune and save an audio file of the results.

# Installation
```
conda create -n themeTuneRemover python=3.6
conda activate themeTuneRemover
pip install -r requirements.txt
```

# Usage


```shell
python audio_offset_finder.py --find-offset-of //path-to-target.wav --within //path-to-containing.wav
```


# Note:
If you get an IndexError: Index out of bounds then you'll need to update the `readers.py` file in the moviepy env directory.
Insert the code from this pull request into readers.py: https://github.com/Zulko/moviepy/pull/1757/files
