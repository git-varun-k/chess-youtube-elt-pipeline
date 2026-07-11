import requests
import json
import os 
from dotenv import load_dotenv
from datetime import date

load_dotenv(dotenv_path='./.env')

CHANNEL_HANDLE='chess'
YOUR_API_KEY=os.getenv('YOUR_API_KEY')
maxResults = 50

def get_playlist_id():
    
    try:
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={YOUR_API_KEY}'

        response=requests.get(url)

        response.raise_for_status()

        data=response.json()

        # print(json.dumps(data, indent=4))

        # channel_items = data["items"][0]

        channel_playlists_Id=data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        
        # print(channel_playlists_Id)

        return channel_playlists_Id
    
    except requests.exceptions.RequestException as e:
        raise e
    

def get_video_ids(playlist_id):

    try:
        max_results=50

        base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlist_id}&key={YOUR_API_KEY}"

        response=requests.get(base_url)
        response.raise_for_status()
        data=response.json()

        video_ids=[]

        for item in data["items"]:
            video_ids.append(item["contentDetails"]["videoId"])

        while("nextPageToken" in data):
            nextPageToken=data["nextPageToken"]
            url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&pageToken={nextPageToken}&playlistId={playlist_id}&key={YOUR_API_KEY}"
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()
            for item in data["items"]:
                video_ids.append(item["contentDetails"]["videoId"])

                    
        return video_ids

    except requests.exceptions.RequestException as e:
        raise e


def extract_video_data(video_ids):

    extracted_data=[]
    
    def batch_list(video_id_lst, batch_size):
        for start in range(0, len(video_id_lst), batch_size):
            yield video_id_lst[start: start + batch_size]

    try:
        for batch in batch_list(video_ids, maxResults):
            video_ids_str = ",".join(batch)

            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={YOUR_API_KEY}"

            response=requests.get(url)
            response.raise_for_status()
            data=response.json()

            for item in data.get('items', []):
                video_id = item["id"]
                snippet = item["snippet"]
                contentDetails = item["contentDetails"]
                statistics = item["statistics"]

                video_data = {
                    "video_id": video_id,
                    "title": snippet["title"],
                    "publishedAt": snippet["publishedAt"],
                    "duration": contentDetails["duration"],
                    "viewCount": statistics.get("viewCount", None),
                    "likeCount": statistics.get("likeCount", None),
                    "commentCount": statistics.get("commentCount", None)
                }

                extracted_data.append(video_data)
        
        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e

def save_to_json(extracted_data):
    file_path = f"./data/YT_data_{date.today()}.json"

    with open(file_path, 'w', encoding='utf-8') as json_outfile:
        json.dump(extracted_data, json_outfile, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    video_data = extract_video_data(video_ids)
    save_to_json(video_data)