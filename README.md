# Simple Screen Recorder
A screen recorder written in `Python` with `ffmpeg` as backend.

![IMG_1304](https://user-images.githubusercontent.com/4103880/128118476-2a6f9a83-925f-4c17-8f0e-d47194f0c520.PNG)


## Advantages
- It's simple.
- Of course, no live stream functionalities. (eg. OBS, Google Meets, etc.)
- Lightweight (53MB), don't need to be installed, cracked, etc. (and open source :D)
- Uses less resources. (~15% of CPU, 100MB of RAM)
- Export video as MKV and auto convert it into MP4 and delete the MKV file. (MKV file won't be corrupted when the program crashes. If it crashed, you can use "Convert to MP4" feature in the program.
- Resolution, quality of the video can be configured.
- Small file size (auto bitrate, auto framedrop if duplicated, ~150MB for a 30-minutes video (tested with 1280x1024 screen resolution, quality 60%))
- "Downscale" feature, allows you to reduce video resolution, quality in order to decrease file size.

## Disadvantages
- Again, it's simple, bad UI.
- No audio recording.
- Console logs can not be closed (minimize only).
- Source code is not clean, hard to read.
- And bugssss :))

## Using the source code
- Make sure you have `PySimpleGUI` library installed and put [`ffmpeg.exe`](https://ffmpeg.org/download.html) in the same directory.
```bash
pip install PySimpleGUI
```
- Then run `screenrecorder.py` file.
- That's it :D

## Notes
- If there are bugs or you want to add new features, feel free to open an issue and I will try to fix/add them if I can.

## Credits
- Me :))
- Python, ffmpeg, PySimpleGUI.
- Google, Stack Overflow and moreee...