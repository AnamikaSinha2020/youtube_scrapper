import json
import googleapiclient.discovery
import json
import logging

import boto3

# api_key = 'AIzaSyCARkUF_v4pNmyQFMbuQ_XBpiuE0ofvD_Y'
# api_key = 'AIzaSyAwjigDbbAlx1boxpbHL08Nx774OsVQyjQ'
api_key = 'AIzaSyB1hJWOCnKwHs9r3_dxzPCxzvsEEsSVA9I'
# api_key = 'AIzaSyDfwjMhx-JNp0VjduxyaTn4VlX3T-VWqWQ'

s3 = boto3.resource('s3')
BUCKET = "Youtube-Anamika"

def build_youtube(API_KEY):
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY)
    return youtube


def search_videos(youtube, channel_id, page_token):
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        # channelId = ','.join(channel_id),
        type="video",
        pageToken=None
    )
    response = request.execute()
    return response


def search_comments(youtube, video_id, page_token):
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        pageToken=page_token
    )

    response = request.execute()
    return response



def process_search_response(response):
    next_page_token = response.get('nextPageToken')
    result = []
    for i, item in enumerate(response["items"]):
        video_id = item["id"]["videoId"]
        video_title = item['snippet']['title']
        channel_id = item['snippet']['channelId']
        description = item['snippet']['description']
        thumbnail = item['snippet']['thumbnails']['default']['url'],
        video_upld_date = item['snippet']['publishTime']
        result.append({
            'video_id': video_id,
            'video_title': video_title,
            'channel_id' : channel_id,
            'video_desc' : description,
            'thumbnail' : thumbnail[0],
            'video_upld_date' : video_upld_date
        })
    return next_page_token, result


def process_comments_response(response, video):
    next_page_token = response.get('nextPageToken')
    result = []
    for i, item in enumerate(response["items"]):
        comment = item["snippet"]["topLevelComment"]
        author = comment["snippet"]["authorDisplayName"]  # Use Later
        comment_text = comment["snippet"]["textDisplay"]
        video_id = video['video_id']
        video_title = video['video_title']
        result.append(
            {
                'video_id': video_id,
                'video_title': video_title,
                'author': author,
                'comment_text': comment_text
            }
        )

    return next_page_token, result


def search_statistics(youtube, video_id, page_token):
    request = youtube.videos().list(
        part="snippet, statistics",
        id=video_id,
        pageToken=page_token
    )

    response = request.execute()
    return response





def process_statistics_response(response, video):
    # next_page_token = response.get('nextPageToken')
    result = []
    for i, item in enumerate(response["items"]):
        likes = item['statistics']['likeCount']
        video_id = video['video_id']
        video_title = video['video_title']
        result.append(
            {
                'video_id': video_id,
                'video_title': video_title,
                'likes': likes,
            }
            )

    return result