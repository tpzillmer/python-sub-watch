import praw

reddit = praw.Reddit(client_id='GWQCwKgHbzFZYw',
                     client_secret=None,
                     user_agent='test')

def watchSubforKey(sub, keyList):
    currentTitle = ''
    try:
        while(True):
            for submission in reddit.subreddit(sub).new(limit=1):
                title = submission.title
                if title != currentTitle:
                    currentTitle = title
                    for keyword in keyList:
                        if keyword in title:
                            print("A mention of {} has been posted in {}.".format(keyword, sub))
                            
    except KeyboardInterrupt:
        print("Done watching")

if __name__ == "__main__":
    keyList = []
    
    sub = input("Please enter a subreddit you would like to watch: ")
    key = input("Please enter a keyword you would like to watch for in {}: ".format(sub))
    keyList.append(key)
    
    while(key.lower() != 'no'):
        key = input('Would you like to watch for an additional keyword? If not, enter "no": ')
        if(key.lower()!='no'):
            keyList.append(key)

    watchSubforKey(sub, keyList)
