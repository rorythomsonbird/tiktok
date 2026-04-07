"""
videorender.py — Generate TTS audio and render the final TikTok video.

Uses edge-tts (free Microsoft neural voices) instead of gTTS.
Install: pip install edge-tts moviepy Pillow
"""

import asyncio
import os
import random
import shutil
import time
from typing import Optional

import edge_tts
from moviepy.editor import (
    AudioFileClip, CompositeAudioClip, CompositeVideoClip,
    ImageClip, TextClip, VideoFileClip,
    concatenate_audioclips, concatenate_videoclips,
)
import moviepy.video.fx.all as vfx
from moviepy.config import change_settings
from PIL import Image, ImageDraw, ImageFont

from config import (
    IMAGEMAGICK_PATH, BACKGROUND_VIDEO, OUTPUT_VIDEO,
    CAPTION_TEMPLATE, FONT_FILE,
    TTS_VOICE, VIDEO_WIDTH, VIDEO_HEIGHT,
    TEXT_FONTSIZE, TEXT_COLOR, TEXT_Y_POSITION, MAX_BG_OFFSET,
)

change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_PATH})

TEMP_DIR = "temp_assets"


# ── TTS ────────────────────────────────────────────────────────────────────────

async def _tts_chunk(text: str, outfile: str, voice: str) -> None:
    """Generate a single TTS audio file using edge-tts."""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(outfile)


def generate_tts_files(chunks: list[str], voice: str = TTS_VOICE) -> list[str]:
    """
    Generate one MP3 per text chunk.
    Returns list of audio file paths in order.
    """
    os.makedirs(TEMP_DIR, exist_ok=True)
    audio_files = []
    for i, chunk in enumerate(chunks):
        if not chunk.strip():
            continue
        path = os.path.join(TEMP_DIR, f"audio_{i:03d}.mp3")

        # retry edge-tts transient failure up to 4 times
        retry_count = 4
        for attempt in range(1, retry_count + 1):
            try:
                asyncio.run(_tts_chunk(chunk.strip(), path, voice))
                break
            except Exception as e:
                print(f"[TTS] chunk {i+1}/{len(chunks)} attempt {attempt} failed: {e}")
                if attempt == retry_count:
                    raise
                time.sleep(2 ** attempt)

        audio_files.append(path)
        print(f"  [TTS] chunk {i+1}/{len(chunks)}: {chunk[:50]}")
    return audio_files


# ── Caption image ──────────────────────────────────────────────────────────────

def make_caption_image(outfile: str, caption: str) -> None:
    """
    Render a caption PNG by compositing text onto captiontemplate.png.
    Automatically shrinks font if the caption is very long.
    """
    words = caption.split()
    # Insert line breaks every ~8 words
    lines, line = [], []
    for word in words:
        line.append(word)
        if len(line) >= 8:
            lines.append(" ".join(line))
            line = []
    if line:
        lines.append(" ".join(line))
    formatted = "\n".join(lines)

    fontsize = max(14, 22 - max(0, len(lines) - 2) * 3)

    image = Image.open(CAPTION_TEMPLATE).convert("RGBA")
    overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
    font = ImageFont.truetype(FONT_FILE, fontsize)
    draw = ImageDraw.Draw(overlay)
    draw.text((10, 60), formatted, font=font, fill=(0, 0, 0, 255))
    combined = Image.alpha_composite(image, overlay)
    combined.save(outfile, "PNG")
    print(f"[Caption] Saved to {outfile}")


# ── Full video render ──────────────────────────────────────────────────────────

def render_video(
    chunks: list[str],
    title: str,
    bg_video_path: str   = BACKGROUND_VIDEO,
    outfile: str         = OUTPUT_VIDEO,
    caption_image: Optional[str] = None,
    bg_offset: Optional[int] = None,
) -> str:
    """
    Full pipeline: TTS → audio stitch → text clips → composite with background.
    Returns the output file path.
    """
    if bg_offset is None:
        bg_offset = random.randint(0, MAX_BG_OFFSET)

    # 1. Generate TTS
    print("[Render] Generating TTS audio...")
    audio_files = generate_tts_files(chunks)
    if not audio_files:
        raise ValueError("No audio files generated — chunks list may be empty.")

    # 2. Load audio clips and measure durations
    audio_clips = [AudioFileClip(f) for f in audio_files]
    durations   = [c.duration for c in audio_clips]
    total_dur   = sum(durations)

    # 3. Stitch audio to one file
    stitched_audio = concatenate_audioclips(audio_clips)
    stitched_path  = os.path.join(TEMP_DIR, "stitched_audio.mp3")
    stitched_audio.write_audiofile(stitched_path, fps=44100, verbose=False, logger=None)
    for c in audio_clips:
        c.close()
    stitched_audio.close()

    # 4. Build text clips (one per chunk, shown for its audio duration)
    print("[Render] Building text clips...")
    text_clips = []
    t = 0
    for i, (chunk, dur) in enumerate(zip(chunks, durations)):
        if not chunk.strip():
            continue
        tc = (
            TextClip(
                chunk,
                font      = FONT_FILE,
                fontsize  = TEXT_FONTSIZE,
                color     = TEXT_COLOR,
                align     = "center",
                method    = "caption",
                size      = (VIDEO_WIDTH - 60, None),
            )
            .set_start(t)
            .set_duration(dur)
        )
        text_clips.append(tc)
        t += dur

    # 5. Load + crop background
    print("[Render] Processing background video...")
    bg = VideoFileClip(bg_video_path).subclip(bg_offset, bg_offset + total_dur)
    bg = vfx.resize(bg, newsize=(1980, 1280))
    bg = bg.crop(x_center=1980 / 2, y_center=1280 / 2, width=VIDEO_WIDTH, height=VIDEO_HEIGHT)

    # 6. Composite layers
    layers = [bg]
    if caption_image and os.path.exists(caption_image):
        img_clip = (
            ImageClip(caption_image)
            .set_duration(total_dur)
            .set_position(("center", "center"))
            .resize(1.2)
        )
        layers.append(img_clip)

    text_composite = CompositeVideoClip(text_clips, size=(VIDEO_WIDTH, VIDEO_HEIGHT)).set_position(("center", TEXT_Y_POSITION))
    layers.append(text_composite)

    final = CompositeVideoClip(layers, size=(VIDEO_WIDTH, VIDEO_HEIGHT))
    final = final.set_audio(AudioFileClip(stitched_path).subclip(0, total_dur))

    # 7. Write output to temporary file; avoid leaving stale output on failure
    tmp_outfile = outfile + ".tmp.mp4"
    print(f"[Render] Writing video to {tmp_outfile} ...")
    try:
        final.write_videofile(tmp_outfile, audio_codec="aac", verbose=False, logger=None)
        final.close()

        # move final file into place
        if os.path.exists(outfile):
            os.remove(outfile)
        os.replace(tmp_outfile, outfile)

        # 8. Cleanup temp
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
        print("[Render] Done.")
        return outfile
    except Exception as e:
        print(f"[Render] Error writing output: {e}")
        if os.path.exists(tmp_outfile):
            os.remove(tmp_outfile)
        raise
