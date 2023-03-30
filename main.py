# Hightown - Spotify to MP3
# Created by Timo Wielink and ChatGPT
# GitHub: https://github.com/TimoWielink

import os
import sys
import spotipy
import spotipy.util as util
import yt_dlp
from difflib import SequenceMatcher
from tqdm import tqdm

# Set up the Spotify API client
SPOTIFY_USERNAME = os.getenv('SPOTIFY_USERNAME')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

scope = 'playlist-read-private'

token = util.prompt_for_user_token(SPOTIFY_USERNAME, scope,
                                   client_id=SPOTIFY_CLIENT_ID,
                                   client_secret=SPOTIFY_CLIENT_SECRET,
                                   redirect_uri=SPOTIFY_REDIRECT_URI)

if not token:
    print('Failed to retrieve Spotify access token.')
    sys.exit(1)

sp = spotipy.Spotify(auth=token)

# Set up the YouTube downloader
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
}

# Get the user's playlists
playlists = sp.current_user_playlists()

# Print the names of the playlists
print('Playlists:')
for i, playlist in enumerate(playlists['items']):
    print(f'{i+1}. {playlist["name"]}')

# Ask the user to select a playlist
playlist_index = int(input('Enter the number of the playlist you want to download: ')) - 1
selected_playlist = playlists['items'][playlist_index]

# Get the name of the selected playlist
playlist_name = selected_playlist['name']

# Get the tracks in the selected playlist
tracks = sp.playlist_tracks(selected_playlist['id'])


# Get the names of the tracks and artists in the selected playlist
track_info = [(track['track']['name'], track['track']['artists'][0]['name']) for track in tracks['items']]

# Search for each track on YouTube and download the audio
video_urls_and_titles = []
for track_name, artist_name in track_info:
    # Search for the track on YouTube
    search_query = f'{track_name} {artist_name} audio'
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(f'ytsearch:{search_query}', download=False)['entries']

    # Find the video URL that best matches the track name
    best_match = None
    for result in search_results:
        similarity = SequenceMatcher(None, track_name.lower(), result['title'].lower()).ratio()
        if not best_match or similarity > best_match['similarity']:
            best_match = {'url': result['webpage_url'], 'title': result['title'], 'similarity': similarity}

    video_urls_and_titles.append((best_match['url'], best_match['title'], artist_name))



    # Download the songs
print('Downloading songs...')
for i, (video_url, song_title, artist_name) in enumerate(tqdm(video_urls_and_titles)):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{playlist_name}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    tqdm.write(f'{song_title} downloaded ({i+1}/{len(video_urls_and_titles)})')

    # Print a success message
print(f'\nAll songs from playlist "{playlist_name}" downloaded successfully!')
