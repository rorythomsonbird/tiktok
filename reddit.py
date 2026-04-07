"""
reddit.py — Fetch and prepare Reddit stories.
"""

import unicodedata
import re
import praw
from config import (
    REDDIT_CREDS_FILE, STORY_URLS_FILE,
    STORY_TITLE_FILE, STORY_BODY_FILE,
    BAD_WORDS_FILE, SUBREDDIT
)


def _load_reddit() -> praw.Reddit:
    """Read credentials from file and return an authenticated Reddit instance."""
    lines = open(REDDIT_CREDS_FILE, "r", encoding="utf-8").read().splitlines()
    creds = {}
    for line in lines:
        if "=" in line:
            key, value = line.split("=", 1)
        elif ":" in line:
            key, value = line.split(":", 1)
        else:
            continue
        creds[key.strip().lower()] = value.strip()

    # Allow alternate key names from old workspace format
    alias_map = {
        "id": "client_id",
        "secret": "client_secret",
        "user": "username",
        "pass": "password",
        "agent": "user_agent",
    }
    for old_key, standard_key in alias_map.items():
        if standard_key not in creds and old_key in creds:
            creds[standard_key] = creds[old_key]

    required = ["client_id", "client_secret", "username", "password", "user_agent"]
    missing = [k for k in required if k not in creds or not creds[k]]
    if missing:
        raise RuntimeError(
            f"Missing Reddit credentials in {REDDIT_CREDS_FILE}: {', '.join(missing)}. "
            "Expected keys: client_id, client_secret, username, password, user_agent"
        )
    return praw.Reddit(
        client_id     = creds["client_id"],
        client_secret = creds["client_secret"],
        username      = creds["username"],
        password      = creds["password"],
        user_agent    = creds["user_agent"],
    )


def _censor(text: str) -> str:
    """Replace bad words using badwords.txt."""
    try:
        words = open(BAD_WORDS_FILE, "r").read().splitlines()
    except FileNotFoundError:
        return text
    for word in words:
        censored = word[:1] + "ee" + word[1:]
        text = re.sub(re.escape(word), censored, text, flags=re.IGNORECASE)
    text = re.sub(r'\basshole\b', 'A hole', text, flags=re.IGNORECASE)
    return text


def _clean_text(text: str) -> str:
    """Normalise unicode, strip problematic characters."""
    text = unicodedata.normalize("NFC", text)
    # Remove characters that cause TTS or MoviePy issues
    text = text.replace("\u2019", "'").replace("\u2018", "'")  # curly quotes
    text = text.replace("\u2014", " - ").replace("\u2013", " - ")  # em/en dash
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)   # strip remaining non-ASCII
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _split_into_sentences(text: str) -> list[str]:
    """
    Split body text into short sentence-boundary chunks suitable for TTS+captions.
    Tries to keep chunks around 12 words — splitting at sentence ends first,
    then by comma if a sentence is too long.
    """
    # Split on sentence-ending punctuation
    raw_sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    for sentence in raw_sentences:
        words = sentence.split()
        if not words:
            continue
        # If the sentence is short enough, keep as-is
        if len(words) <= 14:
            chunks.append(sentence.strip())
        else:
            # Break long sentences at commas first, then hard-split
            parts = re.split(r',\s+', sentence)
            current = []
            for part in parts:
                current.append(part)
                if len(" ".join(current).split()) >= 10:
                    chunks.append(", ".join(current).strip())
                    current = []
            if current:
                chunks.append(", ".join(current).strip())
    return [c for c in chunks if c]


def fetch_story() -> dict:
    """
    Fetch the next unseen top story from SUBREDDIT.
    Saves title/body to files and records the URL.
    Returns {"title": str, "body": str, "chunks": list[str]}.
    Raises RuntimeError if no new story is found.
    """
    reddit = _load_reddit()
    stored_urls = set(open(STORY_URLS_FILE, "r").read().splitlines())

    for post in reddit.subreddit(SUBREDDIT).top(limit=None):
        if post.url in stored_urls or not post.selftext:
            continue

        title = _clean_text(post.title)
        body  = _censor(_clean_text(post.selftext))
        chunks = _split_into_sentences(body)

        # Persist
        open(STORY_TITLE_FILE, "w", encoding="utf-8").write(title)
        open(STORY_BODY_FILE,  "w", encoding="utf-8").write(body)
        with open(STORY_URLS_FILE, "a") as f:
            f.write(post.url + "\n")

        print(f"[Reddit] Fetched: {title[:60]}...")
        return {"title": title, "body": body, "chunks": chunks}

    raise RuntimeError("No new stories found — all top posts have been used.")
