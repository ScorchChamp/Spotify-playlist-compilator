from spotifyAPI import spotifyAPI
from youtubeAPI import youtubeAPI
import ffmpegWrapper as fw
sapi = spotifyAPI()
yapi = youtubeAPI()

playlistID = '37i9dQZF1DWWF3yivn1m3D'

for item in sapi.getPlaylistItems(playlistID):
    url = yapi.downloadVideo(item)
    urlWithTitle = fw.addTextOverlay(url, item.title, -20, 20, 20)
    urlWithTitleAndAuthor = fw.addTextOverlay(urlWithTitle, item.title, -20, 20, 20)
videoPaths = [ ]