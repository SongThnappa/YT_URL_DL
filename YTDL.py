import os
import requests
import json
from googleapiclient.discovery import build

def load_api_key():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        return config['youtube_api_key']

# Function to get the "Uploads" playlist ID from a channel
def get_uploads_playlist_id(api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    )
    response = request.execute()
    
    uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return uploads_playlist_id

# Function to get video URLs from a YouTube playlist
def get_video_urls_from_playlist(api_key, playlist_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_urls = []
    
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()
    
    while request is not None:
        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_urls.append(f"https://www.youtube.com/watch?v={video_id}")
        
        request = youtube.playlistItems().list_next(request, response)
        if request:
            response = request.execute()
    
    return video_urls

# Main function to run the script
def main():
    api_key = load_api_key()  # Load the API key from config file
    channel_id = "YOUR_CHANNEL_ID"  # Replace with your YouTube channel ID
    
    # Get the "Uploads" playlist ID
    uploads_playlist_id = get_uploads_playlist_id(api_key, channel_id)
    print(f"Uploads playlist ID: {uploads_playlist_id}")
    
    # Get all video URLs from the "Uploads" playlist
    video_urls = get_video_urls_from_playlist(api_key, uploads_playlist_id)
    
    # Print or save the video URLs
    for url in video_urls:
        print(url)

    # Optionally, save the URLs to a file
    with open("video_urls.txt", "w") as file:
        for url in video_urls:
            file.write(url + "\n")
    print("Video URLs have been saved to video_urls.txt")

if __name__ == "__main__":
    main()