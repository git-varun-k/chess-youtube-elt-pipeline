from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.video_stats import get_playlist_id, get_video_ids, extract_video_data, save_to_json

local_tz = pendulum.timezone("Europe/Berlin")

default_args={
    'owner':"datakeeper",
    'depends_on_past':False,
    'email_on_failure': False,
    'email_on_retry': False,
    'email': "keeper@gmail.com",
    # 'retries':1,
    # 'retry_delay':timedelta(minutes=5),
    'max_active_runs':1,
    'dagrun_timeout': timedelta(hours=1),
    'start_date': datetime(2026, 1, 1, tzinfo=local_tz),
    # 'end_date': datetime(2030, 12, 31 tzinfo=local_tz),
}

with DAG(
    dag_id="produce_json",
    default_args=default_args,
    description="DAG to produce JSON file with raw data",
    schedule="0 14 * * *",
    catchup=False,
) as dag:
    
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extract_data = extract_video_data(video_ids)
    fetch_json = save_to_json(extract_data)

    playlist_id >> video_ids >> extract_data >> fetch_json