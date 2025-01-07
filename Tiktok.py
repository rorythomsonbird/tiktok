from Upload import Upload
from Videorender import Videorender
from Reddit import Reddit
import os, sys, time
import random


class SuppressPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

Reddit.story("AITAH")
video_background_file = "C:\\Users\\roryt\\Desktop\\Code\\tiktokbot\\tiktok\\minecraftback.mp4"
video_background_offset = random.randint(0, 500) 
output_file = "C:\\Users\\roryt\\Desktop\\Code\\tiktokbot\\tiktok\\AutoClip_Out.mp4" 
content = open("storybody.txt","r").read()
cap = open("storytitle.txt","r").read()
Videorender.makecaption("newcap.png", cap)
Videorender.clip(content=content, 
     video_file=video_background_file, 
     image_file="C:\\Users\\roryt\\Desktop\\Code\\tiktokbot\\tiktok\\newcap.png",
     outfile=output_file, 
     offset=video_background_offset)


print("Logging in...")
with SuppressPrints():
    driver = Upload.login()
if driver == "error":
    print("There was a problem, please retry.")
else:
    print("Login success!")
    print("Beginning upload...")
    try:
        Upload.upload(driver,"C:\\Users\\roryt\\Desktop\\Code\\tiktokbot\\tiktok\\AutoClip_Out.mp4")

    except Exception:
        print("ERROR UPLOADING")
        print(Exception)
        time.sleep(300)
        driver.quit()




