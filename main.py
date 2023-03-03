from spotifyAPI import spotifyAPI
from youtubeAPI import youtubeAPI
import googleAPI
import ffmpegWrapper as fw
import os
import datetime
import sys
import string
import thumbnailGenerator as tg

sapi = spotifyAPI()
yapi = youtubeAPI()
SNIPPET_LENGTH, FADE_LENGTH = 10, 0.5
BASE_DIR = f'{os.path.dirname(os.path.abspath(__file__))}'


def run(playlistID, channelID):
    LIST_FILE = f'{BASE_DIR}/videos/{playlistID}.txt'
    pData = sapi.getPlaylistData(playlistID)
    NOW = datetime.datetime.now()
    title = string.capwords(f"{str(pData['name']).upper()} - {NOW.strftime('%B')} {NOW.year}")
    print(title, pData['description'])

    videoPaths = []
    index = 0
    items = sapi.getPlaylistItems(playlistID)[:3]
    print("Generating thumbnail")
    thumbnail = sapi.downloadImage(pData['images'][0]['url'], playlistID)
    thumbnail = tg.generateThumbnail(thumbnail, string.capwords(pData['name']))
    for item in items:
        print(str(item))
        index += 1
        try: url = yapi.downloadVideo(item)
        except: continue
        videoLength = fw.getVideoLength(url)
        snippetLength = SNIPPET_LENGTH if index != 1 else SNIPPET_LENGTH*2
        video = fw.cutVideo(
            url, (videoLength/2) - (snippetLength/2), snippetLength, FADE_LENGTH)
        if item.blacklisted:
            video = fw.blurVideo(video)
        video = fw.addTextOverlay(video, [(f"{index}. {item.title}", 100, 150, 64, 'Roboto-Regular.ttf'),
                                  (', '.join(item.artists), 100, 75, 52, 'Roboto-Thin.ttf')] + ([("Cannot play this song due to copyright", 320, 540, 78, 'Roboto-Thin.ttf')] if item.blacklisted else []), videoLength, FADE_LENGTH)
        videoPaths.append(video)

    videoPaths.reverse()
    print("Generating intro")
    videoPaths[0] = fw.addImageOverlay(videoPaths[0], thumbnail, 2)

    with open(LIST_FILE, 'w') as f:
        for file in videoPaths:
            f.write(f"""file 'file:{file}'\n""")

    resultFile = fw.concatVideos(LIST_FILE, f'{playlistID}.mp4')
    print(pData['description'], pData['name'], pData['images'])

    description = f"""
{pData['description']}

#Spotify #Music #Top 
"""
    tags = ["Spotify", "Music", "Top"] + \
        [str(item).replace(":", "-")[:20] for item in items][:15]

    videoId = googleAPI.uploadVideo(title, description, tags, googleAPI.getUploadDateISO(
        2023, NOW.month, NOW.day, 18, 0), '10', resultFile, channelID, premiere=True)

    googleAPI.upload_thumbnail(channelID, videoId, thumbnail)

playlistID = sys.argv[1]
run(playlistID, 'UC6HPYeFSbNkL9FFVhdA9UFg')
