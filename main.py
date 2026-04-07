"""
main.py — Orchestrate the full Reddit → Video → TikTok pipeline.

Usage:
    python main.py            # full pipeline
    python main.py --render   # render video only (no upload)
    python main.py --upload   # upload only (uses existing AutoClip_Out.mp4)
    python main.py --login    # open browser to login manually (do this first!)
"""

import argparse
import os
import sys
import time

from config import (
    OUTPUT_VIDEO,
    BACKGROUND_VIDEO,
    SUBREDDIT,
    STORY_TITLE_FILE,
    YOUTUBE_DESCRIPTION_TEMPLATE,
    YOUTUBE_TAGS,
)
from reddit import fetch_story
from videorender import make_caption_image, render_video
from upload import login, upload_video
from youtube_upload import upload_to_youtube


def run_full_pipeline():
    print("=" * 55)
    print("  TikTok Bot — Full Pipeline")
    print("=" * 55)

    # ── 1. Fetch story ─────────────────────────────────────────────────────────
    print("\n[1/3] Fetching Reddit story...")
    try:
        story = fetch_story()
    except RuntimeError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    # ── 2. Render video ────────────────────────────────────────────────────────
    print("\n[2/3] Rendering video...")
    caption_img = "newcap.png"
    make_caption_image(caption_img, story["title"])
    render_video(
        chunks        = story["chunks"],
        title         = story["title"],
        bg_video_path = BACKGROUND_VIDEO,
        outfile       = OUTPUT_VIDEO,
        caption_image = caption_img,
    )

    # ── 3. Verify render output exists before upload ───────────────────────────
    if not os.path.exists(OUTPUT_VIDEO) or os.path.getsize(OUTPUT_VIDEO) == 0:
        print(f"[ERROR] Render did not produce a valid video at {OUTPUT_VIDEO}. Aborting upload.")
        sys.exit(1)

    print("\n[3/3] Uploading to TikTok...")
    driver = login()
    tiktok_success = upload_video(driver, OUTPUT_VIDEO)
    if not tiktok_success:
        print("[ERROR] TikTok upload failed. Will still attempt YouTube upload.")
        time.sleep(5)
    driver.quit()

    print("\n[4/4] Uploading to YouTube...")
    try:
        upload_to_youtube(
            OUTPUT_VIDEO,
            story["title"],
            YOUTUBE_DESCRIPTION_TEMPLATE.format(title=story["title"]),
            YOUTUBE_TAGS,
        )
        print("\n✓ YouTube upload complete!")
    except Exception as e:
        print(f"[ERROR] YouTube upload failed: {e}")
        print("\n✗ Pipeline finished with errors.")
        sys.exit(1)

    print("\n✓ Pipeline complete!")

def run_full_pipeline_youtube():
    print("=" * 55)
    print("  YouTube Shorts Bot — Full Pipeline")
    print("=" * 55)

    # ── 1. Fetch story ─────────────────────────────────────────────────────────
    print("\n[1/3] Fetching Reddit story...")
    try:
        story = fetch_story()
    except RuntimeError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    # ── 2. Render video ────────────────────────────────────────────────────────
    print("\n[2/3] Rendering video...")
    caption_img = "newcap.png"
    make_caption_image(caption_img, story["title"])
    render_video(
        chunks        = story["chunks"],
        title         = story["title"],
        bg_video_path = BACKGROUND_VIDEO,
        outfile       = OUTPUT_VIDEO,
        caption_image = caption_img,
    )

    # ── 3. Verify render output exists before upload ───────────────────────────
    if not os.path.exists(OUTPUT_VIDEO) or os.path.getsize(OUTPUT_VIDEO) == 0:
        print(f"[ERROR] Render did not produce a valid video at {OUTPUT_VIDEO}. Aborting upload.")
        sys.exit(1)

    print("\n[3/3] Uploading to YouTube...")
    upload_to_youtube(
        OUTPUT_VIDEO,
        story["title"],
        YOUTUBE_DESCRIPTION_TEMPLATE.format(title=story["title"]),
        YOUTUBE_TAGS,
    )
    print("\n✓ YouTube upload complete!")


def run_render_only():
    print("[Mode] Render only")
    story = fetch_story()
    caption_img = "newcap.png"
    make_caption_image(caption_img, story["title"])
    render_video(
        chunks        = story["chunks"],
        title         = story["title"],
        bg_video_path = BACKGROUND_VIDEO,
        outfile       = OUTPUT_VIDEO,
        caption_image = caption_img,
    )
    print(f"Video saved to: {OUTPUT_VIDEO}")


def run_upload_only():
    print("[Mode] TikTok upload only")

    if not os.path.exists(OUTPUT_VIDEO) or os.path.getsize(OUTPUT_VIDEO) == 0:
        print(f"[ERROR] Output video not found or empty at {OUTPUT_VIDEO}. Run --render first.")
        return

    driver = login()
    success = upload_video(driver, OUTPUT_VIDEO)
    if not success:
        print("[ERROR] Upload failed.")
        time.sleep(30)
    driver.quit()


def run_youtube_upload_only():
    print("[Mode] YouTube upload only")

    if not os.path.exists(OUTPUT_VIDEO) or os.path.getsize(OUTPUT_VIDEO) == 0:
        print(f"[ERROR] Output video not found or empty at {OUTPUT_VIDEO}. Run --render first.")
        return

    title = os.path.splitext(os.path.basename(OUTPUT_VIDEO))[0]
    if os.path.exists(STORY_TITLE_FILE):
        try:
            saved_title = open(STORY_TITLE_FILE, "r", encoding="utf-8").read().strip()
            if saved_title:
                title = saved_title
        except Exception:
            pass

    if not title:
        title = "Reddit Short Story"

    upload_to_youtube(
        OUTPUT_VIDEO,
        title,
        YOUTUBE_DESCRIPTION_TEMPLATE.format(title=title),
        YOUTUBE_TAGS,
    )


def run_login_only():
    print("[Mode] Login — browser will open, log in manually, then close it.")
    driver = login()
    input("Press Enter once you are fully logged in to TikTok...")
    driver.quit()
    print("Profile saved. You won't need to log in again.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TikTok Reddit Bot")
    parser.add_argument("--render", action="store_true", help="Render video only")
    parser.add_argument("--upload", action="store_true", help="Upload existing video only")
    parser.add_argument("--login",  action="store_true", help="Open browser to log in")
    parser.add_argument("--youtube", action="store_true", help="Use YouTube upload instead of TikTok")
    args = parser.parse_args()

    if args.login:
        run_login_only()
    elif args.render and args.youtube:
        print("[ERROR] --render and --youtube cannot be combined")
        sys.exit(1)
    elif args.render:
        run_render_only()
    elif args.upload and args.youtube:
        run_youtube_upload_only()
    elif args.upload:
        run_upload_only()
    elif args.youtube:
        run_full_pipeline_youtube()
    else:
        run_full_pipeline()
