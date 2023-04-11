# Spotify To MP3

A simple Python script to download songs from a Spotify playlist and convert them to MP3.

## Prerequisites

- Python 3
- A Spotify account
- A Spotify developer account
- FFmpeg (if not already installed)

## Setup

1. Clone this repository and `cd` into it.

`$ git clone https://github.com/timo-wielink/spotify-to-mp3.git`
`$ cd spotify-to-mp3`


2. Create a virtual environment.

`$ python3 -m venv env`
`$ source env/bin/activate`


3. Install the required Python packages.

`$ pip install -r requirements.txt`


4. Set up the Spotify API credentials.

   - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and create a new app.
   - Add `http://localhost:8080` as a Redirect URI in the app settings.
   - Set the following environment variables with your app's credentials:
   
`SPOTIFY_USERNAME=<your Spotify username>`
`SPOTIFY_CLIENT_ID=<your Spotify client ID>`
`SPOTIFY_CLIENT_SECRET=<your Spotify client secret>`
`SPOTIFY_REDIRECT_URI=http://localhost:8080`


Note: You can also create a `.env` file in the root directory of the project and add the environment variables there.

5. Run the script.

`$ python main.py`


## Usage

1. The script will display a list of your Spotify playlists. Enter the number of the playlist you want to download.
2. The script will prompt you to select where you want to save the downloaded songs. You can choose to save them in the current directory, in the default Music folder, or in a custom folder.
3. The script will download each song from the selected playlist and convert it to MP3.

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please [open an issue](https://github.com/timo-wielink/spotify-to-mp3/issues/new).


