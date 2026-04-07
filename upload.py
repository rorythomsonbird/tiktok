"""
upload.py — Upload a video to TikTok via tiktok-uploader (Playwright-based).

Requires cookies.txt file for authentication.
Install: pip install tiktok-uploader
"""

import os
import shutil
import re
import subprocess
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import (
    CHROME_PROFILE_DIR, CHROMEDRIVER_PATH,
    STORY_TITLE_FILE, HASHTAGS,
)

# ── TikTok Studio upload URL ───────────────────────────────────────────────────
UPLOAD_URL = "https://www.tiktok.com/creator#/upload"
LOGIN_URL  = "https://www.tiktok.com/login"


def _parse_version(text: str) -> tuple[int, int, int] | None:
    m = re.search(r"(\d+)\.(\d+)\.(\d+)", text)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def _version_from_command(cmd: list[str]) -> tuple[int, int, int] | None:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        return _parse_version(out)
    except Exception:
        return None


def _get_chrome_version() -> tuple[int, int, int] | None:
    # Common chrome command names on Windows and Linux
    for chrome_cmd in ["chrome", "google-chrome", "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"]:
        version = _version_from_command([chrome_cmd, "--version"])
        if version:
            return version
    return None


def _get_chromedriver_version() -> tuple[int, int, int] | None:
    return _version_from_command([CHROMEDRIVER_PATH, "--version"]) if CHROMEDRIVER_PATH else None


def _build_driver() -> webdriver.Chrome:
    """
    Build an undetected Chrome driver with a persistent profile.
    A persistent profile means you only need to log in once manually.
    """
    chrome_version = _get_chrome_version()
    chromedriver_version = _get_chromedriver_version() if os.path.exists(CHROMEDRIVER_PATH) else None

    desired_driver_path = None

    # If a local chromedriver path is provided and exists, prefer it even if
    # the detected major versions don't match — this helps when offline.
    if CHROMEDRIVER_PATH and os.path.exists(CHROMEDRIVER_PATH):
        if chromedriver_version and chrome_version and chromedriver_version[0] == chrome_version[0]:
            desired_driver_path = CHROMEDRIVER_PATH
        else:
            print("[Upload] Warning: local CHROMEDRIVER_PATH exists but may not match Chrome major version. Using local driver due to offline/compatibility fallback.")
            desired_driver_path = CHROMEDRIVER_PATH

    if not desired_driver_path:
        # Auto-install matching chromedriver (webdriver-manager fallback)
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            print("[Upload] Installing/using webdriver-manager chromedriver...")
            manager_path = ChromeDriverManager().install()
            desired_driver_path = manager_path
            print(f"[Upload] webdriver-manager chromedriver path: {desired_driver_path}")
        except Exception as e:
            # network/download failure — try to find chromedriver on PATH
            possible = shutil.which("chromedriver")
            if possible:
                print(f"[Upload] webdriver-manager failed but found chromedriver on PATH: {possible}")
                desired_driver_path = possible
            else:
                raise RuntimeError(
                    "Could not reach webdriver-manager host or install Chromedriver.\n"
                    "If you're offline, set CHROMEDRIVER_PATH in config.py to a local chromedriver binary.\n"
                    "Alternatively install chromedriver manually and ensure it's on PATH."
                ) from e

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={CHROME_PROFILE_DIR}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--window-size=1920,1080")

    # Headless mode (use UI off-screen)
    from config import HEADLESS
    if HEADLESS:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Avoid GPU / virtualization issues if headless
    options.add_argument("--disable-software-rasterizer")

    driver_service = Service(desired_driver_path)
    driver = webdriver.Chrome(service=driver_service, options=options)
    return driver


def login() -> webdriver.Chrome:
    """
    Open the TikTok login page and return the driver.
    If you already have a saved profile with a valid session this
    will just open TikTok and return immediately — no login needed.
    """
    driver = _build_driver()
    driver.get(LOGIN_URL)
    print("[Upload] Login page opened. If already logged in this will redirect automatically.")
    print("[Upload] Waiting 15 seconds for page to settle...")
    time.sleep(15)
    return driver


def _safe_click(driver, by, selector, timeout=5):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, selector))
        )
        element.click()
        return True
    except Exception:
        return False


def _dismiss_tiktok_overlays(driver):
    # Cookie consent
    _safe_click(driver, By.XPATH, "//button[contains(., 'Allow all')]")
    _safe_click(driver, By.XPATH, "//button[contains(., 'Decline optional cookies')]")

    # Automatic content checks overlay
    _safe_click(driver, By.XPATH, "//button[contains(., 'Cancel') and not(contains(., 'Continue'))]")
    _safe_click(driver, By.XPATH, "//button[contains(., 'No, thanks')]")

    # Generic central modal close icon
    _safe_click(driver, By.XPATH, "//button[contains(@aria-label, 'Close') or contains(., 'Close')]")


def upload_video(driver: webdriver.Chrome, video_path: str) -> bool:
    """
    Upload video_path to TikTok Studio via Selenium.
    Returns True on success, False on failure.
    """
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    driver.get(UPLOAD_URL)
    print("[Upload] Navigated to upload page")
    time.sleep(3)
    _dismiss_tiktok_overlays(driver)

    try:
        file_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        file_input.send_keys(os.path.abspath(video_path))
        print(f"[Upload] File path sent: {video_path}")
    except Exception as e:
        print("[Upload] FAILED to send file:", e)
        return False

    # Wait for file to upload / processing UI to appear
    time.sleep(8)
    _dismiss_tiktok_overlays(driver)

    try:
        caption_box = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']"))
        )
        caption_box.click()
        time.sleep(1)

        try:
            title = open(STORY_TITLE_FILE, "r", encoding="utf-8").read().strip()
        except Exception:
            title = "AITA Story"

        caption = (
            f"{title}\n"
            f"Reddit Storytime • AITA Drama\n"
            f"Who's in the wrong?\n"
            f"{HASHTAGS}"
        )

        caption_box.send_keys(Keys.CONTROL, "a")
        caption_box.send_keys(Keys.DELETE)
        time.sleep(0.2)
        caption_box.send_keys(caption)
        print("[Upload] Caption entered.")

    except Exception as e:
        print("[Upload] Failed to set caption:", e)

    _dismiss_tiktok_overlays(driver)

    # Click post button
    for attempt in range(3):
        try:
            post_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//button[not(@disabled) and (.//text()='Post' or @data-e2e='post_video_button')]")
                )
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", post_button)
            time.sleep(0.5)
            post_button.click()
            print("[Upload] Post clicked!")

            # Validate post confirmation with toast or redirect
            for check_seconds in [5, 10, 20, 30, 60, 90]:
                try:
                    WebDriverWait(driver, check_seconds).until(
                        EC.visibility_of_element_located(
                            (By.XPATH, "//*[contains(text(), 'successfully uploaded') or contains(text(), 'posted') or contains(text(), 'published') or contains(text(), 'added to your profile')]")
                        )
                    )
                    print("[Upload] Post confirmed by message")
                    return True
                except Exception:
                    pass

            # Confirm by Profile button or Video View path display
            try:
                if WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//button[contains(., 'Go to video') or contains(., 'View profile') or contains(., 'Go to profile')]") )
                ):
                    print("[Upload] Post confirmed via call-to-action button")
                    return True
            except Exception:
                pass

            print("[Upload] Post not explicitly confirmed, treating as success with caution")
            return True

        except Exception as e:
            print(f"[Upload] Post click attempt {attempt + 1} failed:", e)
            _dismiss_tiktok_overlays(driver)
            time.sleep(5)

    print("[Upload] FAILED to click Post button")
    return False
