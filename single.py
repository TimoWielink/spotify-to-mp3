import os
import sys
import yt_dlp
from difflib import SequenceMatcher

print("""
 __  __ ____ _____   ____   _____        ___   _ _        _    ___  ____  _____ ____  
|  \/  |  _ \___ /  |  _ \ / _ \ \      / / \ | | |      / \  / _ \|  _ \| ____|  _ \ 
| |\/| | |_) ||_ \  | | | | | | \ \ /\ / /|  \| | |     / _ \| | | | | | |  _| | |_) |
| |  | |  __/___) | | |_| | |_| |\ V  V / | |\  | |___ / ___ \ |_| | |_| | |___|  _ < 
|_|  |_|_|  |____/  |____/ \___/  \_/\_/  |_| \_|_____/_/   \_\___/|____/|_____|_| \_\
""")



# Set up the YouTube downloader
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
}


# Ask the user for the name of the song and artist
song_name_and_artist = input('Enter the name of the song and artist (in the format "Song Name - Artist"): ')

# Search for the song on YouTube
search_query = f'{song_name_and_artist} audio'
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    search_results = ydl.extract_info(f'ytsearch:{search_query}', download=False)['entries']

# Find the video URL that best matches the input
best_match = None
for result in search_results:
    similarity = SequenceMatcher(None, song_name_and_artist.lower(), f"{result['title']} - {result['uploader']}").ratio()
    if not best_match or similarity > best_match['similarity']:
        best_match = {'url': result['webpage_url'], 'title': result['title'], 'uploader': result['uploader'], 'similarity': similarity}

# Confirm that the video being downloaded is the correct one
print(f"Is this the correct video to download? (Y/N)\nTitle: {best_match['title']}\nUploader: {best_match['uploader']}")
confirm_download = input().lower()

if confirm_download == 'y':
    # Ask the user where to save the downloaded song
    # Set up the output file path based on user's selection
    output_option = input('Enter the number of the option you want to select:\n'
                          '1. Save downloaded file in current directory\n'
                          '2. Save downloaded file in default Music Folder\n'
                          '3. Enter custom file path\n')
    if output_option == '1':
        output_dir = '.'
    elif output_option == '2':
        output_dir = '~/Music'
    else:
        output_dir = input('Enter the file path where you want to save the downloaded file: ')

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Download the song
    print('Downloading song...')
    ydl_opts['outtmpl'] = f'{output_dir}/{best_match["title"]}.%(ext)s'
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([best_match['url']])
    print(f'{best_match["title"]} downloaded successfully!')

else:
    print('Download cancelled.')    
