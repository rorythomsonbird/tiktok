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

video_background_file = "C:\\Users\\roryt\\Desktop\\Code\\tiktokbot\\tiktok\\minecraftback.mp4"
video_background_offset = random.randint(0, 500) 
output_file = "C:\\Users\\roryt\\Desktop\\Code\\tiktokbot\\tiktok\\AutoClip_Out.mp4" 
content = """My son(30) and his fiancée(28) of six years 
go on a family trip every year with her extended family. 
From what my son tells me, 
they travel to different locations 
and rent an Airbnb that accommodates 
the 30 people who attend. 
For the past three years, 
they’ve gone during the holidays, 
and as a result, we rarely see them. 
My future daughter-in-law (DIL) 
and I have a good relationship, 
but I can’t say we talk much.

My son and his fiancée are planning 
a trip in March for spring break, 
and I asked my son when we might 
be able to plan a trip together in the future. 
He mentioned there might be enough room at 
the house they’re staying at. 
I told him that sounded great and asked him 
to let me know the costs for everyone attending. 
My 24-year-old son, 22-year-old daughter, 
and 3-year-old grandson also live with me, 
so we all planned to go.

A few days later, my son told me that we’d
likely have to sleep on a couch or share one
 of the kids’ bunk beds if they were available. 
 I assured him we’d make it work, 
 and I sent him our share of the costs. 
 I also told my kids, 
 who were very excited—this would be their 
 first vacation that’s more than a three-hour car ride away.

Last week, my son called and told me it wouldn’t 
work for us to join them after all, 
and he sent back the deposit. 
When I asked why, he explained that his fiancée didn’t 
feel comfortable with us coming. 
She was upset because I didn’t attend her engagement 
dinner last year to meet her side of the family, 
which she felt would make it awkward 
to share the vacation rental. 
She was also upset that I didn’t reach out to her
directly to discuss joining the trip, 
leaving my son to relay the information instead.

I told my son it was fine, but I ended up booking 
a hotel about 15 miles from where they’re staying. 
I also told my son he didn’t have to worry about 
making time to see us. 
Now, my DIL is upset because she feels that we’re
 still somehow taking away from their trip.

Am I The Asshole?

EDIT::: I should have noted my dil’s mom recently 
passed away and since our relationship has been feeling more strained. 
I did not attend the funeral for those who ask, 
and I reach out to my son because i don’t want to bother her. 
it’s clear she doesn’t like us much and bitter.
"""
#cap = "AITA for booking a hotel in the same area as my son and dil’s trip that we didn’t get to go on?"
#Videorender.makecaption("newcap.png", cap)
#Videorender.clip(content=content, 
#     video_file=video_background_file, 
#     image_file="C:\\Users\\roryt\\Desktop\\Code\\tiktokbot\\tiktok\\newcap.png",
#     outfile=output_file, 
#     offset=video_background_offset)
#print("Logging in...")
#with SuppressPrints():
#    driver = Upload.login()
#if driver == "error":
#    print("There was a problem, please retry.")
#else:
#    print("Login success!")
#    print("Beginning upload...")
#    try:
#        Upload.upload(driver,"C:\\Users\\roryt\\Desktop\\Code\\tiktokbot\\tiktok\\AutoClip_Out.mp4")
#
#    except Exception:
#        print("ERROR UPLOADING")
#        print(Exception)
#        time.sleep(300)
#        driver.quit()

Reddit.story("AITAH")


