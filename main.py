import json
import logging
import googleapiclient.discovery
from pytube import YouTube as yt_youtube
from utils import build_youtube, search_videos, search_comments, process_search_response, process_comments_response, api_key, search_statistics, process_statistics_response, s3, BUCKET
from file_upload import download_upload_video
import pandas as pd
from db_connection import cursor, mydb

def main(api_key):
    # READING API and CHANNEL ID from config.json

    # config_file_name = "configvideo_title.json"
    # with open(config_file_name) as config_file:
    #    config = json.load(config_file)

    api_key = api_key
    # channel_id = ['UCNU_lfiiWBdtULKOw6X0Dig', 'UC59K-uG2A5ogwIrHw4bmlEg', 'https://www.youtube.com/watch?v=WMolA7QMP5w', 'UCkGS_3D0HEzfflFnG0bD24A']
    channel_id = 'UCNU_lfiiWBdtULKOw6X0Dig'
    # channelId = "\'UCNU_lfiiWBdtULKOw6X0Dig\', \'UC59K-uG2A5ogwIrHw4bmlEg\', \'https://www.youtube.com/watch?v=WMolA7QMP5w\', \'UCkGS_3D0HEzfflFnG0bD24A\'"

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
        next_page =None
        if not next_page:
            break
    print(videos)
    count_v1 = 0
    for video in videos:
        next_page = None
        while True:
            response_comment = search_comments(youtube, video['video_id'], next_page)
            next_page, result_comments = process_comments_response(response_comment, video)
            comments += result_comments
            count_v1 += 1
            if not next_page:
                break
            if count_v1 >= 3:
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
    comments, likes, videos = main(api_key)
    df_videos = pd.DataFrame.from_records(videos)
    df_videos['video_link'] = df_videos.apply(lambda row: f"https://www.youtube.com/watch?v={row['video_id']}", axis=1)

    df_videos['video_url_s3'] = df_videos.apply(lambda row: download_upload_video(row['video_link'], s3, BUCKET), axis = 1)
    df_likes = pd.DataFrame.from_records(likes)
    df_merged = pd.merge(df_videos, df_likes[['video_id', 'likes']], on='video_id')

    dict_video = df_merged.T.to_dict().values()
    for data in dict_video:
        upload_date = data['video_upld_date'].replace('Z', '').replace('T', ' ')
        query = f"""insert into YTscraper.Video_tbl (video_id, Channel_id, Video_title, 
        Videao_link, Video_disc, Thumb_nail, Likes, Video_url, 
        Video_upload_date) values("{data['video_id']}", "{data['channel_id']}", "{data['video_title']}", "{data['video_link']}", "{data['video_desc']}", "{data['thumbnail']}", "{data['likes']}", "{data['video_url_s3']}", "{upload_date}")
        ON DUPLICATE KEY UPDATE
        Channel_id = "{data['channel_id']}",
        Video_title = "{data['video_title']}",
        Videao_link = "{data['video_link']}",
        Video_disc = "{data['video_desc']}",
        Thumb_nail = "{data['thumbnail']}",
        Likes = "{data['likes']}",
        Video_url = "{data['video_url_s3']}",
        Video_upload_date = "{upload_date}" """;
        print(query)

        cursor.execute(query)
        mydb.commit()

    for data in comments:
        comment_upd = data['comment_text'].replace("\"", "")
        query = f"""insert into `YTscraper`.Commenter_tbl (video_id, Commentor_name, Comments, video_title) 
        values("{data['video_id']}", "{data['author']}", "{comment_upd}" , "{data['video_title']}")
        ON DUPLICATE KEY UPDATE 
        Commentor_name = "{data['author']}",
        Comments = "{comment_upd}",
        video_title =  "{data['video_title']}" """;
        print(query)

        cursor.execute(query)
        mydb.commit()