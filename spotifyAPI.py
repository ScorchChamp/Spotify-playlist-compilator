import os
import dotenv
import base64
import requests
import hashlib
import yaml
from yaml.loader import SafeLoader
import googletrans
import re

DESC_COVER_REG = r'[C-c]over.*$'
DESC_HTML_REG = r'<.*?>'

class spotifySong:
    videoURL = ''

    def __init__(self, data):
        self._data = data
        self._id = data['id']
        self._artists = data['artists']
        self._track = data['track']

    @property
    def title(self):
        return self._data['name']

    @property
    def artists(self):
        return [artist['name'] for artist in self._data['artists']]

    @property
    def fileName(self):
        return hashlib.sha256(str(self).encode()).hexdigest()

    @property
    def blacklisted(self):
        with open('./settings.yml') as f:
            return self._id in yaml.load(f, Loader=SafeLoader)['blacklisted_tracks']

    def __repr__(self):
        return f"<SpotifySong {self.__str__()}>"

    def __str__(self):
        return f"{self.title} by {', '.join(self.artists)}"


class spotifyAPI:
    ATRequestURL = 'https://accounts.spotify.com/api/token'
    PIRequestURL = 'https://api.spotify.com/v1/playlists/{}/tracks?market=US'
    PRequestURL = 'https://api.spotify.com/v1/playlists/{}?market=US'
    grantType = 'client_credentials'

    def __init__(self):
        dotenv.load_dotenv()

    def getPlaylistItems(self, playlistID):
        responseCode = 0
        tries = 0
        maxTries = 5
        while responseCode != 200:
            tries += 1
            if tries > maxTries:
                raise Exception(f"Failed to get playlist data after {maxTries} tries")
            result = requests.get(self.PIRequestURL.format(playlistID), headers=self.APIRequestHeaders)
            responseCode = result.status_code
            print(responseCode)
        return [spotifySong(item['track']) for item in result.json()['items']]

    def getPlaylistData(self, playlistID):
        responseCode = 0
        tries = 0
        maxTries = 5
        while responseCode != 200:
            tries += 1
            if tries > maxTries:
                raise Exception(f"Failed to get playlist data after {maxTries} tries")
            result = requests.get(self.PRequestURL.format(playlistID), headers=self.APIRequestHeaders)
            responseCode = result.status_code
            print(responseCode)
        result = result.json()
        translator = googletrans.Translator()
        result['description'] = re.sub(DESC_HTML_REG, '', result['description'])
        result['description'] = re.sub(DESC_COVER_REG, '', result['description'])
        result['description'] = translator.translate(result['description'], dest='en').text
        result['name'] = translator.translate(result['name'], dest='en').text
        return result


    @property
    def accessToken(self):
        result = requests.post(self.ATRequestURL, data=self.requestBody, headers=self.ATRequestHeaders)
        return result.json()

    @property
    def clientID(self):
        return os.getenv('CLIENT_ID')

    @property
    def clientSecret(self):
        return os.getenv('CLIENT_SECRET')

    @property
    def APIRequestHeaders(self):
        OAUTH = self.accessToken
        return {
            'Authorization': f"{OAUTH['token_type']} {OAUTH['access_token']}",
            'Content-Type': 'application/json'
        }

    @property
    def ATRequestHeaders(self):
        return {
            'Authorization': 'Basic ' + base64.b64encode(f'{self.clientID}:{self.clientSecret}'.encode()).decode(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    @property
    def requestBody(self):
        return {
            'grant_type': 'client_credentials'
        }
