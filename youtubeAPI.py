from pytube import Search
import os
import urllib.request

class youtubeAPI:
    def __init__(self):
        self._videoFolder = '/videos/source/'

    def downloadVideo(self, spotifySong):
        output = f"{self.outputFolder}{spotifySong.fileName}.mp4"
        urllib.request.urlretrieve(self.getVideoDownloadUrl(str(spotifySong)), output) if not os.path.exists(output) else ''
        return output

    def getVideoDownloadUrl(self, title):
        return Search(title).results[0].streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().url

    @property
    def outputFolder(self):
        path = f'{os.path.dirname(os.path.abspath(__file__))}{self._videoFolder}'
        os.makedirs(path, exist_ok=True)
        return path
