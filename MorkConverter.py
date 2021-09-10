import os
import sys
import json
import base64
import ffmpeg

def main():
    videoFlag = False
    if len(sys.argv) > 1:
        inputfilename = sys.argv[1]
    else:
        inputfilename = "mork.ro.har"

    segMax = 0
    f = open(inputfilename,"r",encoding="utf-8")
    jsonData = json.load(f)
    entries = jsonData['log']['entries']

    for entry in entries:
        request = entry['request']
        response = entry['response']
        if request['method'] != 'GET':
            continue  
        if response['content']['mimeType'] == "video/mp4":
            if "/video/" in request['url']:
                videoFlag = True
                if "init" in request['url'] or "seg_" in request['url']:
                    url = request['url']                
                    videoName = url.split("/")[-1].split("?")[0]
                    videoBase64Text = response['content']['text']
                    if "seg_" in videoName:
                        segNum = int(videoName.split("_")[1].split(".")[0]) 
                        if segNum > segMax :
                            segMax = segNum
                    videoFileSeg = open('video_'+videoName+'.temp', 'wb', buffering=0)
                    videoFileSeg.write(base64.b64decode(videoBase64Text))
                    videoFileSeg.close()
            elif "/audio/" in request['url']:
                if "init" in request['url'] or "seg_" in request['url']:
                    url = request['url']                
                    audioName = url.split("/")[-1].split("?")[0]
                    audioBase64Text = response['content']['text']    
                    audioFileSeg = open('audio_'+audioName+'.temp', 'wb', buffering=0)
                    audioFileSeg.write(base64.b64decode(audioBase64Text))
                    audioFileSeg.close()

    f.close()

    if videoFlag == False:
        print("No Video Content Detected!")
        return

    videoFile = open("video.mp4.temp", 'wb', buffering=0)
    audioFile = open("audio.mp4.temp", 'wb', buffering=0)
    initVideo = open("video_init.mp4.temp", 'rb', buffering=0)
    initAudio = open("audio_init.mp4.temp", 'rb', buffering=0)
    videoFile.write(initVideo.read())
    audioFile.write(initAudio.read())
    initVideo.close()
    initAudio.close()

    videoTemp = ffmpeg.input("video_init.mp4.temp")


    if segMax > 0:
        for i in range(1, segMax):
            segVideo = open("video_seg_%s.mp4.temp" % i, 'rb', buffering=0)
            segAudio = open("audio_seg_%s.mp4.temp" % i, 'rb', buffering=0)
            videoFile.write(segVideo.read())
            audioFile.write(segAudio.read())
            segVideo.close()
            segAudio.close()

    videoFile.close()
    audioFile.close()

    try:       
        video = ffmpeg.input('video.mp4.temp')
        audio = ffmpeg.input('audio.mp4.temp')
        output = ffmpeg.output(video, audio, 'output.mp4')
        ffmpeg.run(output, overwrite_output=True)
    except:
        print("ffmpeg Not Found!")

    for (dirpath, dirnames, filenames) in os.walk('./'):
        for filename in filenames:
            if '.mp4.temp' in filename:
                os.remove(filename)


if __name__ == '__main__':
    main()