import praw
import unicodedata
class Reddit:
    
    def initreddit():
        redcred = open("redditcreds.txt","r").read()
        redcredsplit = redcred.split("\n")
        reddit = praw.Reddit(
            client_id=redcredsplit[0].split("=")[1],     
            client_secret=redcredsplit[1].split("=")[1], 
            username=redcredsplit[2].split("=")[1],      
            password=redcredsplit[3].split("=")[1],      
            user_agent=redcredsplit[4].split("=")[1]     
        )
        return reddit

    
    def get_top_stories(reddit, subreddit):
        limit=1
        subreddit = reddit.subreddit(subreddit)
        urls = open("storyurls.txt","r")
        storedurls = urls.read().splitlines()
        top_stories = subreddit.top(limit=None)

        
        titles = []
        bodys = []
        urls = []
        for story in top_stories:
            if story.url not in storedurls:
                titles.append(story.title)
                bodys.append(story.selftext)
                urls.append(story.url+"\n")
                break
        return [titles,bodys,urls]
    
    def story(subreddit):
        reddit = Reddit.initreddit()
        story = Reddit.get_top_stories(reddit, subreddit)
        story[1][0] = unicodedata.normalize('NFC', story[1][0])
        
        story[1][0] = story[1][0].replace("'","")
        story[1][0] = story[1][0].replace("-","")
        open("storytitle.txt","w").write(story[0][0])
        open("storybody.txt","w").write(story[1][0])
        open("storyurls.txt","a").write(story[2][0])

