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


def _do_upload(youtube, video_path: str, title: str, description: str, tags: list, privacy_status: str) -> str:
    """Execute a single resumable upload and return the video ID."""
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
    media = MediaFileUpload(video_path, chunksize=1024 * 1024 * 8, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"[YouTube] Upload progress: {int(status.progress() * 100)}%")

    return response.get("id")


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

    try:
        video_id = _do_upload(youtube, video_path, title, description, tags, privacy_status)
    except Exception as first_error:
        if "invalidTitle" in str(first_error):
            fallback_title = "Reddit Short Story"
            print(f"[YouTube] Title rejected; retrying with fallback: {repr(fallback_title)}")
            video_id = _do_upload(youtube, video_path, fallback_title, description, tags, privacy_status)
        else:
            raise

    print(f"[YouTube] Upload complete. Video ID: {video_id}")
    return video_id