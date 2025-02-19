#    _____     _       _____ _ _     
#   |  _  |_ _| |_ ___|     | |_|___ 
#   |     | | |  _| . |   --| | | . |
#   |__|__|___|_| |___|_____|_|_|  _|
#                            |_| 
#
# By Abhishta (github.com/abhishtagatya)
# Edited for use by Rory Thomson-Bird (github.com/rorythomsonbird)

# pip install gTTs
# pip install moviepy
# pip install rich
# pip install pyfiglet

import os
import random
from typing import List, Tuple

from gtts import gTTS
from moviepy.editor import (
    CompositeVideoClip, CompositeAudioClip,
    VideoFileClip, AudioFileClip, ImageClip, TextClip,
    concatenate_videoclips, concatenate_audioclips
)
import moviepy.video.fx.all as vfx
from rich.console import Console
from rich.progress import track
import pyfiglet
from PIL import Image, ImageDraw, ImageFont
import boto3
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save, stream, Voice, VoiceSettings
from moviepy.config import change_settings 
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

class Videorender:
    def generate_speech(
            text: str, 
            lang: str = 'en', 
            filename: str = 'audio.mp3'):
        """
        Generate Speech Audio from gTTS
        text: str - Text to be synthesized
        lang: str - Language of text
        filename: str - Filename of output
        """
        #polly = boto3.client('polly',region_name='us-east-1')
        #response = polly.synthesize_speech(Text = text, OutputFormat = 'mp3',VoiceId = 'Matthew')

        #with open(filename,'wb') as file:
        #    file.write(response['AudioStream'].read())
        myobj = gTTS(text=text, lang=lang, slow=False, tld='ca') # Change per settings https://gtts.readthedocs.io/en/latest/module.html

        myobj.save(filename)
        return


    def clip(
            content: str, 
            video_file: str, 
            outfile: str, 
            image_file: str = '', 
            offset: int = 0, 
            duration: int = 0):
        """
        Generate the Complete Clip
        content: str - Full content text
        video_file: str - Background video
        outfile: str - Filename of output
        image_file: str - Banner to display
        offset: int - Offset starting point of background video (default: 0)
        duration: int - Limit the video (default: audio length)
        """
        if not os.path.exists("temp_assets"):
            os.mkdir("temp_assets")
        audio_comp, text_comp = Videorender.generate_audio_text(Videorender.split_text(content))

        audio_comp_list = []
        for audio_file in track(audio_comp, description='Stitching Audio...'):
            audio_comp_list.append(AudioFileClip(audio_file))
        audio_comp_stitch = concatenate_audioclips(audio_comp_list)
        audio_comp_stitch.write_audiofile('temp_audio.mp3', fps=44100)

        audio_duration = audio_comp_stitch.duration
        if duration == 0:
            duration = audio_duration

        audio_comp_stitch.close()

        vid_clip = VideoFileClip(video_file).subclip(offset, offset + duration)
        vid_clip = vfx.resize(vid_clip, newsize=(1980, 1280))
        vid_clip = vid_clip.crop(x_center=1980 / 2, y_center=1280 / 2, width=720, height=1280)

        if image_file != '':
            image_clip = ImageClip(image_file).set_duration(duration).set_position(("center", 'center')).resize(1.2) # Adjust if the Banner is too small
            vid_clip = CompositeVideoClip([vid_clip, image_clip])

        vid_clip = CompositeVideoClip([vid_clip, concatenate_videoclips(text_comp).set_position(('center', 860))])

        vid_clip = vid_clip.set_audio(AudioFileClip('temp_audio.mp3').subclip(0, duration))
        vid_clip.write_videofile(outfile, audio_codec='aac')
        vid_clip.close()


    def split_text(text: str, delimiter: str = '\n'):
        """
        Split the Text
        text: str - Text to split
        delimiter: str - Delimiter of split (default: \n)
        """
        return text.split(delimiter)


    def generate_audio_text(fulltext: List[str]):
        """
        Generate Audio and Text from Full Text
        fulltext: List[str] - List of splitted Text
        """
        audio_comp = []
        text_comp = []
        key = open("ttskey.txt","r").read()
        for idx, text in track(enumerate(fulltext), description='Synthesizing Audio...'):
            if text == "":
                continue

            audio_file = f"temp_assets/audio_{idx}.mp3"

            client = ElevenLabs(api_key=key)
            tts = client.generate(
                text=text.strip(),
                voice="Brian"
            )
            save(tts,audio_file)

            audio_duration = AudioFileClip(audio_file).duration

            text_clip = TextClip(
                text,
                font='burbankbigcondensed-bold-1.otf', # Change Font if not found
                fontsize=60,
                color="white",
                align='center',
                method='caption',
                size=(660, None)
            )
            text_clip = text_clip.set_duration(audio_duration)

            audio_comp.append(audio_file)
            text_comp.append(text_clip)

        return audio_comp, text_comp


    def makecaption(name, caption):
        fontsize = 20
        splitcap = caption.split(" ")
        newcap = ""
        for i in range(len(splitcap)):
            if i%9==0 and i!=0:
                newcap = newcap + splitcap[i]+"\n"
                if i >=18:
                    fontsize = fontsize - 5

            else: 
                newcap = newcap + splitcap[i]+" "
        image = Image.open("captiontemplate.png").convert("RGBA")
        txt = Image.new("RGBA", image.size, (255, 255, 255, 0))
        font = ImageFont.truetype("burbankbigcondensed-bold-1.otf", fontsize)
        draw = ImageDraw.Draw(txt)
        draw.text((10,60), newcap, font=font, fill=(0, 0, 0))
        combined = Image.alpha_composite(image, txt)
        combined.save(name, "PNG")


if __name__ == '__main__':

    console = Console()
    

    
    

    video_background_file = "C:\\Users\\roryt\\Desktop\\Code\\tiktokbot\\tiktok\\minecraftback.mp4" # Your video background file
    video_background_offset = random.randint(0, 500) # Starting Position of Video : 0 for Beginning
    output_file = "C:\\Users\\roryt\\Desktop\\Code\\tiktokbot\\tiktok\\AutoClip_Out.mp4" # The output filename

    content = """Hi Reddit. 
    I dont tend to make posts like this
    but I could really use some advice.
    Yesterday Afternoon,
    I made dinner for my parents,
    my dad said my food was bland
    and my mum said shes tasted better
    soup at the homeless shelter.
    So I politely stood up from the table
    and exploded them both with my mind.
    The police said that I probably 
    shouldn't have done that and that
    I'm in the wrong?
    I completely disagree and am currently
    looking for validation.
    So reddit - Am I the asshole? 
    """

    console.print("\n\n[light_green] Task Starting\n\n")
    Videorender.makecaption("newcap.png", "AITA for the way I acted towards my parents when they didn't like my food?")
    Videorender.clip(content=content, 
         video_file=video_background_file, 
         image_file="C:\\Users\\roryt\\Desktop\\Code\\tiktokbot\\tiktok\\newcap.png",
         outfile=output_file, 
         offset=video_background_offset)

    console.print("\n\n[light_green] Completed!")
    
    
    
    
    
    