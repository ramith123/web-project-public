import requests

# from termcolor import colored
from model import Song, Playlist
from random import choice

colors = [
    "(80, 114, 226)",
    "(80, 209, 226)",
    "(80, 226, 102)",
    "(180, 226, 80)",
    "(236, 167, 72)",
    "(236, 84, 72)",
    "(236, 72, 159)",
    "(207, 72, 236)",
    "(147, 72, 236)",
    "(96, 98, 111)",
    "(20, 21, 27)",
]
trackUrl = "https://api.deezer.com/track/"
searchUrl = "https://api.deezer.com/search?q="
youtubeApiKey = "AIzaSyB-0Q-27kT5fOzDo4jjLF5RRXfKgNZI9tU" # You Tube API Key. Invalidated for security
search_url = "https://www.googleapis.com/youtube/v3/search"
youtubeVideoLink = "https://www.youtube.com/watch?v="
playlistUrl = "https://api.deezer.com/playlist/6682665064"  # 1282495565


def getDeezerPlaylist():
    reply = requests.get(playlistUrl)
    data = reply.json()["tracks"]["data"]
    songList = []
    for i, song in enumerate(data):
        track = {
            "id": song["id"],
            "title": song["title"],
            "artist": song["artist"]["name"],
            "album": song["album"]["title"],
            "albumImgUrl": song["album"]["cover_big"],
            "url": song["link"],
            "position": i + 1,
            "playlistId": reply.json()["id"],
        }
        songList.append(track)
    return songList


def getJsonForSearch(query):  # get json data for a search query
    url = searchUrl + query
    reply = requests.get(url)
    return reply.json()["data"]


def getJsonForSongId(id):  # get json data for a search query
    url = trackUrl + id
    reply = requests.get(url)
    return reply.json()


def getSongsList(query=None, data=None):  # get SongList with required information
    if data:
        data = [data]
    else:
        data = getJsonForSearch(query)
    songList = []
    for i, song in enumerate(data):
        track = {
            "id": song["id"],
            "title": song["title"],
            "artist": song["artist"]["name"],
            "album": song["album"]["title"],
            "albumImgUrl": song["album"]["cover_big"],
            "url": song["link"],
        }
        if i < 3:
            track["youtubeUrl"] = getYoutubeLink(song["title"], song["artist"]["name"])

        else:
            track["youtubeUrl"] = getYoutubeLink(
                song["title"], song["artist"]["name"], True
            )
        songList.append(track)
    return songList


def getSongModelById(id):
    data = getJsonForSongId(str(id))
    songList = getSongsList(data=data)
    return getSongModel(songList[0])


def getSongModel(song):  # returns sqlalchemy Song model for a song

    ele = Song(
        id=song["id"],
        title=song["title"],
        artist=song["artist"],
        album=song["album"],
        albumImgUrl=song["albumImgUrl"],
        url=song["url"],
        # youtubeUrl=getYoutubeLink(song["title"], song["artist"])
        youtubeUrl=song["youtubeUrl"],
    )
    return ele


def getYoutubeLink(song, artist, quota=False):
    query = song + " by " + artist
    search_params = {
        "key": youtubeApiKey,
        "q": query,
        "part": "snippet",
        "maxResults": 1,
        "type": "video",
    }
    defaultLink = "https://www.youtube.com/results?search_query=" + query.replace(
        " ", "+"
    )
    defaultLink = defaultLink.replace("'", "")
    if quota:
        return defaultLink
    r = requests.get(search_url, params=search_params)
    try:
        if r.json()["items"]:
            videoId = r.json()["items"][0]["id"]["videoId"]
            return youtubeVideoLink + videoId
        return defaultLink
    except:
        print("got an error from youtube API. Default serach link is stored")
        return defaultLink


def getRandomColor():
    return choice(colors)


youtubePLaylistRequest = None
youtubePLaylistRequest2 = None


def getPlaylistRequest(pageToken=None):
    playlistUrl = "https://www.googleapis.com/youtube/v3/playlistItems"
    parameters = {
        "key": youtubeApiKey,
        "playlistId": "PL4fGSI1pDJn69On1f-8NAvX_CYlx7QyZc",  # Top 100 Music Videos United States(Playlist) on YouTube Music Global Charts channel",
        "part": "snippet,contentDetails",
        "maxResults": 50,
    }
    global youtubePLaylistRequest
    global youtubePLaylistRequest2
    if youtubePLaylistRequest is None:
        youtubePLaylistRequest = requests.get(playlistUrl, params=parameters,)
    if youtubePLaylistRequest2 is None and pageToken:
        parameters["pageToken"] = pageToken
        youtubePLaylistRequest2 = requests.get(playlistUrl, params=parameters,)
        del parameters["pageToken"]

    if pageToken:
        print("R")
        return youtubePLaylistRequest2
    else:
        print("R2")
        return youtubePLaylistRequest


if __name__ == "__main__":
    print(getPlaylistRequest())
    print(youtubePLaylistRequest2)
