import subprocess
import os
BASE_DIR = f'{os.path.dirname(os.path.abspath(__file__))}'

def blurVideo(path):
    outputFile = path.replace(".mp4", f"_blur.mp4")
    os.system(f"""ffmpeg -hide_banner -loglevel error -y -i "{path}" -vf "boxblur=10:2" -an "{outputFile}" """)
    return outputFile

def normalizeText(t: str):
  return t.replace('"', '').replace("'", "").replace(":", "-").replace("%", "*").replace("\\", "\\\\")

def getVideoLength(path):
    return float(subprocess.check_output(f"""ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{path}" """, shell=True).strip().decode("utf-8"))

def cutVideo(path, startTime, cutLength, fadeLength):
    outputFile = path.replace(".mp4", f"_cut.mp4")
    os.system(f"""ffmpeg -hide_banner -loglevel error -y -i "{path}" -ss {startTime} -t {cutLength} -af "volume=loudnorm=I=-14:TP=-2:LRA=11:print_format=summary" -vf "fade=t=in:st={startTime}:d={fadeLength*3},fade=t=out:st={startTime+cutLength-fadeLength}:d={fadeLength},fps=60,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1" -af "afade=t=in:st={startTime}:d={fadeLength*3},afade=t=out:st={startTime+cutLength-fadeLength}:d={fadeLength}" -vcodec libx264 -ar 44100 -c:a aac -b:a 192k -preset ultrafast "{outputFile}" """)
    return outputFile


def addTextOverlay(path, settings, videoLength, fadeLength):
    drawTextSettings = ','.join([f"""drawtext=fontfile={fontPath}:text='{normalizeText(text if len(text) < 40 else text[:38] + '...')}':x={xOffset}:y=h-th-{yOffset}:fontsize={fontSize}:fontcolor=white,fade=t=in:st=0:d={fadeLength*3},fade=t=out:st={videoLength-fadeLength}:d={fadeLength}""" for text, xOffset, yOffset, fontSize, fontPath in settings])
    outputFile = path.replace(".mp4", f"_text.mp4")
    os.system(f"""ffmpeg -hide_banner -loglevel error -y -i "{path}" -vf "{drawTextSettings},fade=t=out:st={videoLength-fadeLength}:d={fadeLength}" "{outputFile}" """)
    return outputFile

def concatVideos(listFile, outputFile):
    outputFile = f"{os.path.dirname(os.path.abspath(__file__))}/videos/{outputFile}"
    os.system(f"""ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i "{listFile}" -c copy "{outputFile}" """)
    return outputFile

def addImageOverlay(video, image, duration):
    outputFile = video.replace(".mp4", f"_overlay.mp4")
    os.system(f"""ffmpeg -hide_banner  -y -i {video} -loop 1 -i "{image}" -filter_complex "[1:v]fade=out:st={duration}:d=1:alpha=1[ovrl]; [0:v][ovrl]overlay=(W-w)/2:(H-h)/2" -shortest -c:a copy "{outputFile}" """)

    # os.system(f"""{BASE_DIR}/ffmpeg -hide_banner -loglevel error -y -i "{video}" -loop 1 -i "{image}" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -shortest -vf "fade=t=in:st=0:d={duration},fade=t=out:st={duration}:d={duration}" "{outputFile}" """)
    return outputFile