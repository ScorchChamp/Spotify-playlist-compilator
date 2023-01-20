from pytube import Search
import os
import urllib.request
import base64


class youtubeAPI:
    def __init__(self):
        self._videoFolder = '/videos/'

    def downloadVideo(self, spotifySong):
        url = self.getVideoDownloadUrl(str(spotifySong))
        output = f"{self.outputFolder}{base64.b64encode(str(spotifySong).encode()).decode().replace('/', '-')}.mp4"
        urllib.request.urlretrieve(url, output) if not os.path.exists(output) else ''
        return output

    def getVideoDownloadUrl(self, title):
        return Search(title).results[0].streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().url

    @property
    def outputFolder(self):
        path = f'{os.path.dirname(os.path.abspath(__file__))}{self._videoFolder}'
        os.mkdir(path) if not os.path.exists(path) else ''
        return path
