import json
import logging
import googleapiclient.discovery
from pytube import YouTube as yt_youtube
from utils import build_youtube, search_videos, search_comments, process_search_response, process_comments_response, api_key, search_statistics, process_statistics_response
import pandas as pd
from db_connection import cursor

def main(api_key):
    # READING API and CHANNEL ID from config.json

    # config_file_name = "configvideo_title.json"
    # with open(config_file_name) as config_file:
    #    config = json.load(config_file)

    api_key = api_key
    channel_id = 'UCnz-ZXXER4jOvuED5trXfEA'

    youtube = build_youtube(api_key)

    videos = []
    comments = []
    likes = []
    # try:
    next_page = None
    while True:
        response = search_videos(youtube, channel_id, next_page)
        next_page, result = process_search_response(response)
        videos += result
        if not next_page:
            break
    print(videos)

    for video in videos:
        next_page = None
        while True:
            response_comment = search_comments(youtube, video['video_id'], next_page)
            next_page, result_comments = process_comments_response(response_comment, video)
            comments += result_comments
            if not next_page:
                break

        print("video ===", video)
        response_likes = search_statistics(youtube, video['video_id'], next_page)
        print("likes ==", response_likes)
        result_likes = process_statistics_response(response_likes, video)
        likes += result_likes
    # except Exception as e:
    #     pass
        # logger.error(f"Error:\n{str(e)}")
    print(f"Total comments: {len(comments)}")
    print(f"Total videos: {len(videos)}")
    print("comments ==", comments)
    print("likes ==", likes)
    return comments, likes, videos




if __name__ == '__main__':
    comments, likes, videos = main(apikey)
    df_videos = pd.DataFrame.from_records(videos)
    df_videos['video_link'] = df_videos.apply(lambda row: f"https://www.youtube.com/watch?v={row['video_id']}", axis=1)

    df_likes = pd.DataFrame.from_records(likes)
    df_merged = pd.merge(df_videos, df_likes[['video_id', 'likes']], on='video_id')

    dict_video = df_merged.T.to_dict().values()
    for data in dict_video:
        query = f"insert into youtube_project.video_tbl (video_id, channel_id, video_title, video_link, video_desc, thumb_nail, likes) values('{data['video_id']}', '{data['channel_id']}', '{data['video_title']}', '{data['video_link']}', '{data['video_desc']}', '{data['thumbnail']}', '{data['likes']}')";
        print(query)

        cursor.execute(query)
        mydb.commit()