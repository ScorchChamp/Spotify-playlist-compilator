import pickle
import os
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import random
import time
from urllib.error import HTTPError
import httplib2
import http
from googleapiclient.http import MediaFileUpload
import logging
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
httplib2.RETRIES = 1
MAX_RETRIES = 10
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
                        http.client.IncompleteRead, http.client.ImproperConnectionState,
                        http.client.CannotSendRequest, http.client.CannotSendHeader,
                        http.client.ResponseNotReady, http.client.BadStatusLine)
services = {}


def createService(channel):
    if channel in services:
        return services[channel]

    client_secret_file = f"{BASE_DIR}/auth/client_secrets.json"
    api_name = 'youtube'
    api_version = 'v3'
    scopes = [['https://www.googleapis.com/auth/youtube']]

    SCOPES = [scope for scope in scopes[0]]

    cred = None

    pickle_file = f'{BASE_DIR}/auth/pickles/{channel}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_file, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(api_name, api_version, credentials=cred)
        print(api_name, 'service created successfully')
        services[channel] = service
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None


def uploadVideo(title, description, tags, uploadDate, categoryID, file, channel, premiere=False):
    logger.info("Uploading video with youtube service")
    print(f"Uploading {file}")
    service = createService(channel)
    mediaFile = MediaFileUpload(file, chunksize=-1, resumable=True)
    response_upload = service.videos().insert(
        part='snippet,status',
        body=getUploadBody(title, description, tags, uploadDate, categoryID),
        media_body=mediaFile
    )
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print("Uploading file " + file)
            print(response_upload)
            status, response = response_upload.next_chunk()
            if response is not None:
                if 'id' in response:
                    video_id = response['id']
                    print(f"Video id '{video_id}' was successfully uploaded.")
                    # if premiere: planPremiere(title, description, uploadDate, categoryID, video_id, service)
                    return response['id']
            else:
                exit("The upload failed with an unexpected response: %s" % response)
        except HTTPError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (
                    e.resp.status, e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occurred: %s" % e

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print("Sleeping %f seconds and then retrying..." % sleep_seconds)
            time.sleep(sleep_seconds)


def getUploadDateISO(year, month, day, hour, minute):
    return datetime.datetime(year, month, day, hour, minute).isoformat()


def planPremiere(title, description, uploadDate, categoryID, video_id, service):
    try:
        broadcast = service.liveBroadcasts().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "scheduledStartTime": uploadDate
                },
                "status": {
                    "privacyStatus": "private"
                }
            }
        ).execute()
        broadcast_id = broadcast["id"]
        stream = service.liveStreams().insert(
            part="snippet,cdn",
            body={
                "snippet": {
                    "title": title
                },
                "cdn": {
                    "format": "1080p",
                    "ingestionType": "rtmp"
                }
            }
        ).execute()
        stream_id = stream["id"]
        service.liveBroadcasts().bind(
            part="id,contentDetails",
            id=broadcast_id,
            streamId=stream_id
        ).execute()
        service.liveBroadcasts().transition(
            broadcastStatus="live",
            id=broadcast_id,
            part="id,status"
        ).execute()

    except Exception as error:
        print(f"An error occurred: {error}")


def getUploadBody(title, description, tags, uploadDate, categoryID):
    return {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': categoryID
        },
        'status': {
            'privacyStatus': 'private',
            'embeddable': True,
            'publicStatsViewable': True,
            "liveBroadcastContent": "upcoming",
            'selfDeclaredMadeForKids': False,
            'publishAt': uploadDate
        },
        'notifySubscribers': True
    }
