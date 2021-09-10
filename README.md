# Mork 影片提取器

## Overview  

從由 [mork.ro](https://mork.ro/) 儲存的HAR檔案中提取影片。  

## Quickstart
1. Clone this repository and install all the requirements:  
    Open terminal and enter the followings
    ```
    git clone https://github.com/crazypatoto/MorkVideoExtractor
    cd MorkVideoExtractor
    pip install -r requirements.txt 
    ```
2. Download ffmpeg [here](http://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z) (for Windows user only).
3. Extract the file you just downloaded and copy `ffmpeg.exe` to the root directory of this repo.
4. Open terminal and run
    ```
    python MorkConverter.py saved.har
    ```
    or (It will automatically looks for `mork.ro.har` under the same folder)
    ```
    python MorkConverter.py
    ```
5. It will output a mp4 video name `output.mp4` if a video resource is found.

## Guide
