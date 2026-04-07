# Copilot Instructions: TikTok Reddit Bot (claudetok)

## What this project does
- Full pipeline: Reddit AITA posts -> text cleanup/censor -> TTS audio -> video render -> TikTok upload.
- Entry point: `main.py` with modes: no flag (full), `--render`, `--upload`, `--login`.
- Main modules:
  - `reddit.py` fetches top posts from `SUBREDDIT` and writes `storytitle.txt`, `storybody.txt`, appends URL to `storyurls.txt`.
  - `videorender.py` makes caption PNG + builds video via `edge-tts`, `moviepy`, `Pillow`.
  - `upload.py` drives TikTok upload via `tiktok-uploader` (Playwright-based) with cookies from `tiktok_cookies.txt`.
  - `config.py` holds all file paths and runtime parameters (IMAGEMAGICK, CHROMEDRIVER, fonts, video dimensions, TIKTOK_COOKIES_FILE etc.).

## Essential local configs and paths (always update before running)
- `config.py`: background video path, output path, caption template, `CHROME_PROFILE_DIR`, `CHROMEDRIVER_PATH`, `IMAGEMAGICK_PATH`.
- `redditcreds.txt`: `client_id/client_secret/username/password/user_agent`
- `storyurls.txt`: tracks used posts to avoid duplicates.
- `badwords.txt`: custom word obfuscation used in `reddit._censor`.

## Dependency highlights
- Python libs: `praw`, `edge-tts`, `moviepy`, `Pillow`, `selenium`, `undetected-chromedriver`.
- System: ImageMagick CLI (`magick`) path set in `config.py`.

## Behavior patterns for code updates
- Text preparation (`reddit._clean_text`) normalizes Unicode, strips non-ASCII and fixes smart quotes/dashes.
- TTS chunking (`_split_into_sentences`) tries sentences up to ~14 words, splits by commas or hard split if longer.
- `render_video`: warns and raises on empty chunks, cleans temp assets, uses output file name from `OUTPUT_VIDEO`.
- Upload uses `tiktok-uploader` library with cookies; requires `tiktok_cookies.txt` in Netscape format.

## Suggested CLI workflows for debugging
- Onboarding login (before upload): `python main.py --login`.
- Render dry-run only: `python main.py --render` then check `config.OUTPUT_VIDEO` and frame overlay.
- Upload only once a video exists: `python main.py --upload`.

## Project-specific gotchas
- `reddit.py` opens `storyurls.txt` as existing file; ensure the file exists (it can be empty) before first run.
- `upload.py` expects `tiktok_cookies.txt` in Netscape format; export from browser after login using "Get cookies.txt" extension.
- `cap` style text rendering in `videorender.make_caption_image` resizes font by line count (8 words per line heuristic).

## When changing logic, update all flow points
1. If subreddit fetch or chunking changes, adjust `reddit.py` + `storyurls.txt` handling.
2. If caption style changes, update `make_caption_image` and/or `main.py` caption image filename usage.
3. If TikTok upload workflow changes in UI, adapt selectors in `upload.py` and keep the same `main.py` mode flags.

## Why this architecture
- Minimal state is persisted in plain text (`storyurls`, `storytitle`, `storybody`) for recoverability.
- Modular stages allow partial re-runs (`--render`, `--upload`).
- Playwright-based upload with cookie auth aims to avoid repeated manual logins and replicate human-like session behavior.

## Additional notes
- No tests present; verifying changes through manual pipeline run is the primary validation path.
- There is no CI in repo; real world behavior must be validated with live Reddit/TikTok credentials.
