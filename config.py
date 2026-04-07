"""
config.py — Edit this file to configure your bot.
All paths, credentials files, and settings live here.
"""

# ── Paths ──────────────────────────────────────────────────────────────────────
BACKGROUND_VIDEO   = r"C:\Users\roryt\Desktop\Code\tiktokbot\tiktok\minecraftback.mp4"
OUTPUT_VIDEO       = r"C:\Users\roryt\Desktop\Code\tiktokbot\tiktok\AutoClip_Out.mp4"
CAPTION_TEMPLATE   = r"C:\Users\roryt\Desktop\Code\tiktokbot\tiktok\captiontemplate.png"
FONT_FILE          = "burbankbigcondensed-bold-1.otf"
CHROME_PROFILE_DIR = r"C:\TikTokProfile2"
CHROMEDRIVER_PATH  = r"C:\chromedriver\chromedriver-win64\chromedriver.exe"
IMAGEMAGICK_PATH   = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"

# ── Credential files ───────────────────────────────────────────────────────────
REDDIT_CREDS_FILE  = "redditcreds.txt"   # client_id=... / client_secret=... etc.
STORY_URLS_FILE    = "storyurls.txt"
STORY_TITLE_FILE   = "storytitle.txt"
STORY_BODY_FILE    = "storybody.txt"
BAD_WORDS_FILE     = "badwords.txt"

# ── Reddit ─────────────────────────────────────────────────────────────────────
SUBREDDIT          = "AITAH"

# ── TTS (edge-tts) ─────────────────────────────────────────────────────────────
# Run `edge-tts --list-voices` to see all options.
# Good free choices: "en-US-GuyNeural", "en-GB-RyanNeural", "en-AU-WilliamNeural"
TTS_VOICE          = "en-US-GuyNeural"

# ── Runtime mode
HEADLESS           = True

# ── Video ──────────────────────────────────────────────────────────────────────
VIDEO_WIDTH        = 720
VIDEO_HEIGHT       = 1280
TEXT_FONTSIZE      = 58
TEXT_COLOR         = "white"
TEXT_Y_POSITION    = 860    # pixels from top
MAX_BG_OFFSET      = 500    # random start point range (seconds)

# ── TikTok ─────────────────────────────────────────────────────────────────────
TIKTOK_COOKIES_FILE = "tiktok_cookies.txt"  # Netscape format cookies for upload

# ── TikTok caption hashtags ────────────────────────────────────────────────────
HASHTAGS = "#aita #redditstories #storytime #amitheasshole #fyp"

# ── YouTube upload configuration ───────────────────────────────────────────────
YOUTUBE_CLIENT_SECRETS_FILE = "youtube_client_secret.json"
YOUTUBE_TOKEN_FILE          = "youtube_token.json"
YOUTUBE_SCOPES              = ["https://www.googleapis.com/auth/youtube.upload"]
YOUTUBE_CATEGORY_ID         = "22"
YOUTUBE_PRIVACY_STATUS      = "public"
YOUTUBE_DESCRIPTION_TEMPLATE = "{title}\nWhat do you think? 🤔\n#shorts"
YOUTUBE_TAGS                = ["aita", "amitheasshole", "shorts", "reddit", "storytime", "drama", "relationship"]
