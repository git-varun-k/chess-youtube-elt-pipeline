import requests
import json
import os 
from dotenv import load_dotenv

load_dotenv(dotenv_path='./.env')

CHANNEL_HANDLE='chess'
YOUR_API_KEY=os.getenv('YOUR_API_KEY')

def get_playlist_id():
    
    try:
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={YOUR_API_KEY}'

        response=requests.get(url)

        response.raise_for_status()

        data=response.json()

        # print(json.dumps(data, indent=4))

        channel_items = data["items"][0]

        channel_playlists_Id=data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        
        print(channel_playlists_Id)

        return channel_playlists_Id
    
    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    get_playlist_id()
