import praw

reddit = praw.Reddit(client_id='ID',
                     client_secret='SECRET',
                     user_agent='AGENT')

currentTitle = ''

def watchSubforKey(sub, key):
    for submission in reddit.subreddit(sub).new(limit=1):
        title = submission.title
        global currentTitle
        if title != currentTitle:
            currentTitle = title
            if key in title:
                print("A mention of {} has been posted in {}".format(key, sub))

if __name__ == "__main__":
    sub = input("Please enter a subreddit you would like to watch: ")
    key = input("Please enter a keyword you would like to watch for in {}: ".format(sub))

    while(1):
        watchSubforKey(sub, key)
