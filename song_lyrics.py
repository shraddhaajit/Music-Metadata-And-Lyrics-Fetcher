import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius
import wikipedia

SPOTIFY_CLIENT_ID = "XXXXX"
SPOTIFY_CLIENT_SECRET = "XXXXX"
GENIUS_ACCESS_TOKEN = "XXXXX"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

genius = lyricsgenius.Genius(
    GENIUS_ACCESS_TOKEN,
    skip_non_songs=True,
    excluded_terms=["(Remix)", "(Live)"],
    remove_section_headers=True,
    timeout=15
)

wikipedia.set_lang("en")

song_query = input("Enter the song name (and artist if you want): ").strip()

results = sp.search(q=song_query, limit=1, type="track")

if not results["tracks"]["items"]:
    print("No track found. Try again.")
    exit()

track = results["tracks"]["items"][0]
track_name = track["name"]
track_artists = ", ".join([artist["name"] for artist in track["artists"]])
main_artist = track["artists"][0]["name"]
album_name = track['album']['name']

artist_data = sp.artist(track['artists'][0]['id'])
artist_followers = artist_data['followers']['total']
artist_popularity = artist_data['popularity']
artist_genres = ", ".join(artist_data['genres'])

print(f"\nFound: {track_name} by {track_artists}")
print(f"Album: {album_name}")
print(f"Release Date: {track['album']['release_date']}")
print(f"Artist Followers: {artist_followers}")
print(f"Artist Popularity: {artist_popularity}")
print(f"Artist Genres: {artist_genres}")

try:
    search_results = wikipedia.search(album_name)
    album_summary = None
    for result in search_results[:5]:
        try:
            album_summary = wikipedia.summary(result, sentences=5)
            if album_summary:
                print(f"\nAbout the album '{result}':\n")
                print(album_summary)
                break
        except (wikipedia.DisambiguationError, wikipedia.PageError):
            continue
    if not album_summary:
        print(f"\nNo Wikipedia page found for album '{album_name}'.")
except Exception as e:
    print(f"\nWikipedia API Error: {e}")

lyrics_text = None
try:
    song = genius.search_song(track_name, main_artist)
    if song and song.lyrics:
        lyrics_text = song.lyrics
        print("\nFull Lyrics:\n")
        print(lyrics_text)
    else:
        print("\nLyrics not found on Genius.")
except Exception as e:
    print(f"\nGenius API Error: {e}")