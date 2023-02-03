from spotifyAPI import spotifyAPI
from youtubeAPI import youtubeAPI
import googleAPI
import ffmpegWrapper as fw
import os
import datetime
import json
import re

sapi = spotifyAPI()
yapi = youtubeAPI()
SNIPPET_LENGTH, FADE_LENGTH = 10, 0.5
BASE_DIR = f'{os.path.dirname(os.path.abspath(__file__))}'

def run(playlistID, channelID):
    LIST_FILE = f'{BASE_DIR}/{playlistID}.txt'
    pData = sapi.getPlaylistData(playlistID)

    # videoPaths = [ ]
    # index = 0
    items = sapi.getPlaylistItems(playlistID)
    # for item in items:
    #     index += 1
    #     url = yapi.downloadVideo(item)
    #     videoLength = fw.getVideoLength(url)
    #     video = fw.cutVideo(url, videoLength/2, SNIPPET_LENGTH if index != 1 else SNIPPET_LENGTH*2, FADE_LENGTH)
    #     video = fw.addTextOverlay(video, [(f"{index}. {item.title}", 100, 150, 64, 'Roboto-Regular.ttf'), (', '.join(item.artists), 100, 75, 52, 'Roboto-Thin.ttf')], videoLength, FADE_LENGTH)
    #     videoPaths.append(video)

    # videoPaths.reverse()
    # with open(LIST_FILE, 'w') as f:
    #     for file in videoPaths:
    #         f.write(f"""file 'file:{file}'\n""")

    # resultFile = fw.concatVideos(LIST_FILE, f'{playlistID}.mp4')
    resultFile = 'E:\ScorchLLC\Spotify-playlist-compilator/videos/37i9dQZF1EQn4jwNIohw50.mp4'
    print(resultFile)
    print(pData['description'], pData['name'], pData['images'])

    NOW = datetime.datetime.now()
    description = f"""
#Spotify #Music #Top 
{pData['description']}
"""
    description = re.sub(re.compile('<.*?>') , '', description)
    title = f"SPOTIFY {str(pData['name']).upper()} - {NOW.strftime('%B')}/{NOW.year}"
    tags = ["Spotify", "Music", "Top"] + [str(item).replace(":", "-")[:20] for item in items][:15]

    print(tags)
    googleAPI.uploadVideo(title, description, tags, googleAPI.getUploadDateISO(2023, NOW.month, NOW.day, 18, 0), '10', resultFile, channelID, premiere=True)


playlistID = input('Playlist ID: ')
run(playlistID, 'UC6HPYeFSbNkL9FFVhdA9UFg')