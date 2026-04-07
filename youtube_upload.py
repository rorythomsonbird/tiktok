import os

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config import (
    YOUTUBE_CATEGORY_ID,
    YOUTUBE_DESCRIPTION_TEMPLATE,
    YOUTUBE_PRIVACY_STATUS,
    YOUTUBE_TAGS,
)
from youtube_auth import get_credentials


def upload_to_youtube(
    video_path: str,
    title: str,
    description: str | None = None,
    tags: list[str] | None = None,
    privacy_status: str = YOUTUBE_PRIVACY_STATUS,
) -> str:
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    title = title.strip().replace("\n", " ").replace("\r", " ")
    if len(title) > 100:
        title = title[:100].rstrip()
    if not title:
        title = "Reddit Short Story"

    if description is None:
        description = YOUTUBE_DESCRIPTION_TEMPLATE.format(title=title)
    if tags is None:
        tags = YOUTUBE_TAGS

    print(f"[YouTube] Upload title: {repr(title)}")
    print(f"[YouTube] Upload description: {repr(description)}")

    creds = get_credentials()
    youtube = build("youtube", "v3", credentials=creds)

    def make_request(video_title: str):
        now_body = {
            "snippet": {
                "title": video_title,
                "description": description,
                "tags": tags,
                "categoryId": YOUTUBE_CATEGORY_ID,
            },
            "status": {
                "privacyStatus": privacy_status,
            },
        }
        media = MediaFileUpload(video_path, chunksize=1024 * 1024 * 8, resumable=True)
        return youtube.videos().insert(part="snippet,status", body=now_body, media_body=media)

    request = make_request(title)
    response = None
    try:
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"[YouTube] Upload progress: {int(status.progress() * 100)}%")
    except Exception as first_error:
        if "invalidTitle" in str(first_error):
            fallback_title = "Reddit Short Story"
            print(f"[YouTube] Title rejected by YouTube; retrying with fallback title: {fallback_title}")
            request = make_request(fallback_title)
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"[YouTube] Upload progress: {int(status.progress() * 100)}%")
        else:
            raise

    media = MediaFileUpload(video_path, chunksize=1024 * 1024 * 8, resumable=True)
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": YOUTUBE_CATEGORY_ID,
        },
        "status": {
            "privacyStatus": privacy_status,
        },
    }

    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"[YouTube] Upload progress: {int(status.progress() * 100)}%")

    video_id = response.get("id")
    print(f"[YouTube] Upload complete. Video ID: {video_id}")
    return video_id
