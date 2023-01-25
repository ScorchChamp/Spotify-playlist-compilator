from spotifyAPI import spotifyAPI
from youtubeAPI import youtubeAPI
import ffmpegWrapper as fw
sapi = spotifyAPI()
yapi = youtubeAPI()

playlistID = '37i9dQZF1DWWF3yivn1m3D'
SNIPPET_LENGTH = 10
FADE_LENGTH = 0.5
LIST_FILE = 'list.txt'

videoPaths = [ ]
index = 0
items = sapi.getPlaylistItems(playlistID)
for item in items:
    index += 1
    url = yapi.downloadVideo(item)
    videoLength = fw.getVideoLength(url)
    video = fw.cutVideo(url, videoLength/2, SNIPPET_LENGTH if index != len(items) else SNIPPET_LENGTH*2, FADE_LENGTH)
    video = fw.addTextOverlay(video, [(f"{index}. {item.title}", 100, 150, 64, 'Roboto-Regular.ttf'), (', '.join(item.artists), 100, 75, 52, 'Roboto-Thin.ttf')], videoLength, FADE_LENGTH)
    videoPaths.append(video)

videoPaths.reverse()
with open(LIST_FILE, 'w') as f:
    for file in videoPaths:
        f.write(f"""file 'file:{file}'\n""")

resultFile = fw.concatVideos(LIST_FILE, f'{playlistID}.mp4')
print(resultFile)